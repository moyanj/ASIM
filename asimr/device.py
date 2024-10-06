import queue
from asimr.constant import MemoryError, ASIMError


class Register:
    def __init__(self, n_GPR=32, struct=True):
        self.pc = 0  # 程序计数器
        self.sr = 0  # 状态寄存器
        self.tc = 0  # 频率计数器
        self._struct = struct
        self._GPR = [0] * n_GPR  # 通用寄存器

    def set(self, n, data: int):
        if 0 <= n < len(self._GPR):
            if self._struct:
                data = data & 0xFF
            self._GPR[n] = data
        else:
            raise ASIMError(f"Register does not exist: r_{n}")

    def get(self, n):
        if 0 <= n < len(self._GPR):
            return self._GPR[n]
        else:
            raise ASIMError(f"Register does not exist: r_{n}")

    def __str__(self):
        # 打印通用寄存器
        gpr_str = "\n".join(f"r{n}: {val:08X}" for n, val in enumerate(self._GPR))
        # 打印其他寄存器状态
        status_str = f"pc: {self.pc:08X}\nsr: {self.sr:08X}\ntc: {self.tc}"
        return (
            f"General Purpose Registers:\n{gpr_str}\n\nSpecial Registers:\n{status_str}"
        )


class Memory:
    def __init__(self, size, strict=False):
        self.size = size
        self.data = [0] * size
        self.strict = strict

    def read(self, address):
        if 0 <= address < self.size:
            return self.data[address]
        else:
            raise MemoryError(f"Nonexistent memory address: {address}")

    def write(self, address, data):
        if 0 <= address < self.size:
            if self.strict:
                data = data & 0xFF
            self.data[address] = data
        else:
            raise MemoryError(f"Nonexistent memory address: {address}")

    def __str__(self):
        # 每16个字节为一块
        memory_str = "\n" + " ".join(f"{byte}" for byte in self.data) + "\n"
        return memory_str


class Stack:
    def __init__(self, size=64):
        self.data = queue.LifoQueue(size)

    def push(self, data: int):
        if self.data.full():
            raise ASIMError("Stack overflow")
        self.data.put(data)

    def pop(self):
        if self.data.empty():
            return 0

        return self.data.get()
