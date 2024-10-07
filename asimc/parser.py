import concurrent.futures
from asimr.constant import InstructionSet, OperandType, Program, GrammarError
from asimr.core import Instruction, Operand
from loguru import logger
from asimc.cache import LRUCache, lru_cache
import base64
import zstandard
import pickle


class Parser:
    def __init__(self, code: str, max_worker=1):
        self.code = code
        self.worker = max_worker  # worker数量
        self.out = Program()

    def divide_list(self, lst, num_parts):
        k, m = divmod(len(lst), num_parts)
        divided_lists = []
        start = 0
        for i in range(num_parts):
            # 计算每个部分的大小，如果还有剩余元素，则当前部分多分配一个
            part_size = k + (1 if i < m else 0)
            # 计算结束索引，确保不会超出列表范围
            end = start + part_size
            # 将子列表添加到结果列表中
            divided_lists.append(lst[start:end])
            # 更新下一个部分的起始索引
            start = end
        return divided_lists

    def parser(self):
        lines = self.code.split("\n")
        num_processes = min(self.worker, len(lines))  # 可以根据实际情况调整进程数

        futures = []
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_processes
        ) as executor:
            for n, part in enumerate(self.divide_list(lines, num_processes)):
                futures.append(executor.submit(self.handler, part, n))

        results = []
        for future in futures:
            out, n = future.result()
            results.append((out, n))

        results = sorted(results, key=lambda x: x[1])
        for out, n in results:
            self.out = self.out + out

    def handler(self, code, n):
        parser = CodeParser()
        parser.parser(code)
        return parser.out, n


class CodeParser:
    def __init__(self):
        self.line = 0  # 行计数器
        self.out = Program()  # 程序对象
        self.cache = LRUCache(128)  # 缓存

    def find_inst(self, name: str):  # 解析操作码
        name = name.upper()
        if name not in InstructionSet.__members__:
            raise GrammarError(
                f"{name} is not a valid instruction.", {"Line": self.line}
            )
        return InstructionSet[name]

    def config_inst(self, line_l):
        if len(line_l) < 1:
            return
        if line_l[0] == ".data_mem":
            logger.debug(f"Set data_mem to {line_l[1]}")
            self.out.data_mem = int(line_l[1])

        elif line_l[0] == ".n_GPR":
            logger.debug(f"Set n_GPR to {line_l[1]}")
            self.out.n_GPR = int(line_l[1])

        elif line_l[0] == ".stack_size":
            logger.debug(f"Set stack_size to {line_l[1]}")
            self.out.stack_size = int(line_l[1])

        elif line_l[0] == ".inst_mem":
            logger.debug(f"Set inst_mem to {line_l[1]}")
            self.out.inst_mem = int(line_l[1])

        elif line_l[0] == ".include_zstd":
            logger.debug(f"Importing a precompiled file: {line_l[1]}")
            self.inc_zstd(line_l)

        elif line_l[0] == ".include_file":
            logger.debug(f"Importing a file: {line_l[1]}")
        else:
            raise GrammarError(
                "Invalid configurations instruction:" + line_l[0], {"Line": self.line}
            )

    def inc_zstd(self, line_l):
        data = base64.b85decode(line_l[2])
        decommpress = zstandard.decompress(data[4:])
        obj = pickle.loads(decommpress)
        self.out.instructions += obj.instructions

    def parsern_operand(self, operands):
        for i in range(0, 3):
            if i >= len(operands):
                break
            print(i)
            op = operands[i]
            if op == "":
                continue

            elif op.startswith("&"):  # 内存地址
                type = OperandType.Memory
                value = op[1:]
                if value.startswith("0x"):
                    value = int(value, 16)
                else:
                    value = int(value)

            elif op.startswith("r_"):  # 寄存器
                type = OperandType.Register
                value = op[2:]
                if value.isdigit():
                    value = int(value)

                    if value >= self.out.n_GPR:
                        raise GrammarError(
                            f"Invalid register: {op}", {"Line": self.line}
                        )

                else:
                    raise GrammarError("Incorrect register.", {"Line": self.line})

            elif op.isdigit():  # 立即数
                type = OperandType.Number
                value = int(op)

            elif op.startswith("0x"):  # 16进制立即数
                type = OperandType.Number
                value = int(op, 16)

            elif op.startswith(";"):  # 注释
                continue

            elif op.startswith("#"):  # 标签
                type = OperandType.Number
                n = self.out.labels.get(op[1:], None)
                if n:
                    value = n
                else:
                    raise GrammarError(
                        f"Label that does not exist: {op[1:]}", {"Line": self.line}
                    )

            else:
                raise GrammarError(f"Incorrect operand type: {op}", {"Line": self.line})

            yield Operand(value, type)

    def parser_l(self, line: str):
        line = line.split(";")[0]  # 去除行尾注释

        line_l = line.split(" ")

        if line in ["", "\n"]:  # 空行
            return

        elif line.startswith(";"):  # 注释
            return

        elif line.startswith("#"):  # 标签定义
            label_name = line[1:].strip()
            if label_name in self.out.labels:
                raise GrammarError(
                    f"Duplicate label: {label_name}", {"Line": self.line}
                )
            self.out.labels[label_name] = len(self.out.instructions)

        elif line.startswith("."):  # 配置指令
            self.config_inst(line_l)

        else:  # 普通指令
            opcode = self.find_inst(line_l[0])
            operands = self.parsern_operand(line_l[1:])  # 解析操作数
            inst = Instruction(opcode, *operands)
            return inst.pack()

    def parser(self, code):
        for l in code:
            l = l.strip()

            if l == "":  # 处理空行
                continue

            res = self.cache.get(l)

            if res == -1:  # 缓存未命中时才执行解析
                result = self.parser_l(l)
                # 在放入缓存前检查result的有效性，避免存储无效结果
                if result:
                    self.cache.put(l, result)
            else:
                result = res

            if result:
                self.out.instructions.append(result)

            self.line += 1
