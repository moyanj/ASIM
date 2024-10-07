from asimr.constant import InstructionSet, OperandType, CPUError
import asimr.instruction as instruction
from asimr.device import Memory, Register, Stack


class Operand:
    def __init__(self, n, type):
        if not isinstance(type, OperandType):
            raise ValueError("type must is OperandType")
        self.value = n
        self.type = type

    def __str__(self):
        return f"Operand({self.value}, {self.type.name})"

    def __repr__(self):
        return self.__str__()


class Instruction:
    def __init__(
        self, opcode: InstructionSet, source=None, target=None, parameter=None
    ):
        self.opcode = opcode
        self.source = source
        self.target = target
        self.parameter = parameter

    def pack(self, to_int=False):
        data = self.opcode.value.to_bytes(1, byteorder="little")  # 1字节
        if self.source:
            source_type = self.source.type.value.to_bytes(
                1, byteorder="little"
            )  # 1字节
            source_address = self.source.value.to_bytes(4, byteorder="little")  # 4字节

            data += source_type + source_address
        else:
            pass
            # data += b"\x00\x00\x00\x00\x00"

        if self.target:
            target_type = self.target.type.value.to_bytes(
                1, byteorder="little"
            )  # 1字节
            target_address = self.target.value.to_bytes(4, byteorder="little")  # 4字节

            data += target_type + target_address
        else:
            pass
            # data += b"\x00\x00\x00\x00\x00"

        if self.parameter:
            parameter_type = self.parameter.type.value.to_bytes(
                1, byteorder="little"
            )  # 1字节
            parameter_value = self.parameter.value.to_bytes(
                4, byteorder="little"
            )  # 4字节

            data += parameter_type + parameter_value
        else:
            pass
            # data += b"\x00\x00\x00\x00\x00"

        if to_int:
            return int.from_bytes(data, byteorder="little")
        else:
            return data

    @classmethod
    def unpack(cls, data, from_int=False):
        if from_int:
            data = data.to_bytes(16, byteorder="little")

        if type(data) == int:
            return cls(InstructionSet.HALT)

        opcode = InstructionSet(int.from_bytes(data[0:1], byteorder="little"))
        offset = 1
        source = None
        target = None

        if len(data) >= offset:
            source_type = OperandType(int.from_bytes(data[1:2], byteorder="little"))
            source_address = int.from_bytes(data[2:6], byteorder="little")
            source = Operand(source_address, source_type)
            offset += 5

        if len(data) >= offset:
            target_type = OperandType(int.from_bytes(data[6:7], byteorder="little"))
            target_address = int.from_bytes(
                data[offset + 1 : offset + 5], byteorder="little"
            )
            target = Operand(target_address, target_type)
            offset += 5

        parameter = None
        if len(data) >= offset:
            parameter_type = OperandType(
                int.from_bytes(data[offset : offset + 1], byteorder="little")
            )
            parameter_value = int.from_bytes(
                data[offset + 1 : offset + 5], byteorder="little"
            )
            parameter = Operand(parameter_value, parameter_type)
            offset += 5

        return cls(opcode, source, target, parameter)

    def __str__(self):
        return f"{self.opcode.name}({self.source}, {self.target}, {self.parameter})"

    def __repr__(self):
        return f"{self.opcode.name}({self.source}, {self.target}, {self.parameter})"


class Core:
    def __init__(
        self, register: Register, data_mem: Memory, inst_mem: Memory, stack: Stack
    ):
        self.register = register
        self.memory = data_mem
        self.instruction_memory = inst_mem
        self.stack = stack

    def run_ins(self, ins):
        ins = Instruction.unpack(ins)
        name = ins.opcode.name
        if hasattr(instruction, name):
            func = getattr(instruction, name)
            func(self, ins)
        else:
            raise CPUError("Unsupported instruction", {"PC[": self.register.pc})

    def run(self):
        while True:
            self.run_ins(self.instruction_memory.read(self.register.pc))
            self.register.tc += 1
            self.register.pc += 1
