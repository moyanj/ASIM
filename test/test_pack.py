import pytest
from asimr.core import Instruction, Operand, InstructionSet, OperandType


def test_pack_unpack():
    # 创建一个指令对象
    opcode = InstructionSet.ADD
    source = Operand(10, OperandType.Register)
    target = Operand(20, OperandType.Memory)
    parameter = Operand(30, OperandType.Number)
    instruction = Instruction(opcode, source, target, parameter)

    # 打包指令
    packed_data = instruction.pack()

    # 解包指令
    unpacked_instruction = Instruction.unpack(packed_data)

    # 验证解包后的指令是否与原始指令相同
    assert unpacked_instruction.opcode == opcode
    assert unpacked_instruction.source.value == source.value
    assert unpacked_instruction.source.type == source.type
    assert unpacked_instruction.target.value == target.value
    assert unpacked_instruction.target.type == target.type
    assert unpacked_instruction.parameter.value == parameter.value
    assert unpacked_instruction.parameter.type == parameter.type


def test_pack_unpack_with_int():
    # 创建一个指令对象
    opcode = InstructionSet.ADD
    source = Operand(10, OperandType.Register)
    target = Operand(20, OperandType.Memory)
    parameter = Operand(30, OperandType.Number)
    instruction = Instruction(opcode, source, target, parameter)

    # 打包指令为整数
    packed_int = instruction.pack(to_int=True)

    # 解包指令
    unpacked_instruction = Instruction.unpack(packed_int, from_int=True)

    # 验证解包后的指令是否与原始指令相同
    assert unpacked_instruction.opcode == opcode
    assert unpacked_instruction.source.value == source.value
    assert unpacked_instruction.source.type == source.type
    assert unpacked_instruction.target.value == target.value
    assert unpacked_instruction.target.type == target.type
    assert unpacked_instruction.parameter.value == parameter.value
    assert unpacked_instruction.parameter.type == parameter.type


def test_unpack_too_much_data():
    # 测试解包过多的数据
    packed_data = (
        (InstructionSet.ADD.value).to_bytes(1, byteorder="little")
        + (OperandType.Register.value).to_bytes(1, byteorder="little")
        + (10).to_bytes(4, byteorder="little")
        + (OperandType.Memory.value).to_bytes(1, byteorder="little")
        + (20).to_bytes(4, byteorder="little")
        + (OperandType.Number.value).to_bytes(1, byteorder="little")
        + (30).to_bytes(4, byteorder="little")
        + b"\x00" * 4
    )  # 额外的数据
    unpacked_instruction = Instruction.unpack(packed_data)
    assert unpacked_instruction.opcode == InstructionSet.ADD
    assert unpacked_instruction.source.value == 10
    assert unpacked_instruction.source.type == OperandType.Register
    assert unpacked_instruction.target.value == 20
    assert unpacked_instruction.target.type == OperandType.Memory
    assert unpacked_instruction.parameter.value == 30
    assert unpacked_instruction.parameter.type == OperandType.Number


def test_operand():
    o = Operand(0, OperandType.Memory)
    assert o.type == OperandType.Memory
    assert o.value == 0


def test_operand_error():
    with pytest.raises(ValueError):
        o = Operand(0, 0)


# 运行测试
if __name__ == "__main__":
    pytest.main()
