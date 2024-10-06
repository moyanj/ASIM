from enum import Enum, auto
import sys
from dataclasses import dataclass, field
import time


class InstructionSet(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return (start - 1) + count

    MOV = auto()  # 移动
    EXC = auto()  # 交换
    ADD = auto()  # 加法
    SUB = auto()  # 减法
    MUL = auto()  # 乘法
    MOD = auto()  # 取余
    PUSH = auto()  # 压栈
    POP = auto()  # 弹栈
    AND = auto()  # 与操作
    OR = auto()  # 或操作
    XOR = auto()  # 异或操作
    NOT = auto()  # 取反
    SHL = auto()  # 左移
    SHR = auto()  # 右移
    CALL = auto()  # TODO: 调用
    RET = auto()  # TODO: 返回
    HALT = auto()  # 关机(模拟器)
    JMP = auto()  # TODO: 无条件跳转
    JNZ = auto()  # TODO: 为 0 时转移
    JZ = auto()  # TODO: 为 1 时转移
    JE = auto()  # TODO: 等于时转移
    JG = auto()  # TODO: 大于转移
    JB = auto()  # TODO: 小于转移
    JNE = auto()  # TODO: 不等于转移
    NOP = auto()  # 无操作
    CPUID = auto()  # TODO: 获取CPU信息
    
    MPC = auto() # TODO: 复制pc寄存器的值
    MSR = auto() # TODO: 复制状态寄存器的值
    MTC = auto() # TODO: 复制频率寄存器的值

    SDF = auto()  # TODO: 定义函数（开始）
    EDF = auto()  # TODO: 定义函数（结束）

    PNC = auto()  # 打印数字
    PAC = auto()  # 打印ASCII码


class OperandType(Enum):
    Memory = 0x0
    Register = 0x1
    Number = 0x2


class SyscallTable(Enum):
    read = auto()  # TODO: 读流
    write = auto()  # TODO: 写流
    get_pid = auto()  # TODO: 获取PID
    exit = auto()  # TODO: 关机(主机)
    getcwd = auto()  # TODO: 获取当前目录
    chdir = auto()  # TODO: 切换目录
    rename = auto()  # TODO: 重命名
    mkdir = auto()  # TODO: 创建目录
    rmdir = auto()  # TODO: 删除目录
    time = auto()  # TODO: 获取时间
    kill = auto()  # TODO: 杀死进程
    socket = auto()  # TODO: 创建套接字
    accept = auto()  # TODO: 运行套接字连接
    listen = auto()  # TODO: 监听套接字
    bind = auto()  # TODO: 绑定端口
    connect = auto()  # TODO: 连接套接字
    send = auto()  # TODO: 发送数据
    close = auto()  # TODO: 关闭
    recv = auto()  # TODO: 接受数据


@dataclass
class Program:
    instructions: list["Instruction"] = field(default_factory=list)
    data_mem: int = 8 * 1024 * 1024
    inst_mem: int = 8 * 1024 * 1024
    n_GPR: int = 16
    stack_size: int = 64
    labels: dict[str, int] = field(default_factory=dict)
    include_file: list[str] = field(default_factory=list)
    compilation_time: int = int(time.time())

    def __add__(self, other: "Program") -> "Program":
        if not isinstance(other, Program):
            return NotImplemented

        self.instructions = self.instructions + other.instructions
        self.data_mem = other.data_mem
        self.inst_mem = other.inst_mem
        self.n_GPR = other.n_GPR
        self.stack_size = other.stack_size
        self.labels.update(other.labels)
        self.include_file = self.include_file + other.include_file
        return self


def error(text):
    print(f"ERROR: {text}")
    sys.exit()


class ASIMError(Exception):
    def __init__(self, msg: str, other: dict = {}):
        self.msg = f"{msg} ("
        for k, v in other.items():
            self.msg += f"{k}: {v}, "
        # 移除最后一个逗号和空格
        self.msg = self.msg.rstrip(", ") + ")"
        super().__init__(self.msg)  # 调用基类的构造函数


class MemoryError(ASIMError):
    pass


class RegisterError(ASIMError):
    pass


class CPUError(ASIMError):
    pass


class GrammarError(ASIMError):
    pass


tmp = {}
