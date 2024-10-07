from asimr.constant import InstructionSet, OperandType, error
import sys
from .utils import get_value, write_value


def HALT(cpu, ins):
    sys.exit()


def PNC(cpu, ins):

    data = get_value(cpu, ins.source)
    sys.stdout.write(str(data))


def PAC(cpu, ins):
    char = get_value(cpu, ins.source)
    sys.stdout.write(chr(char) if isinstance(char, int) else char)


def MOV(cpu, ins):
    source_value = get_value(cpu, ins.source)
    target_type = ins.target.type
    target_address = ins.target.value

    if target_type == OperandType.Register:
        cpu.register.set(target_address, source_value)
    elif target_type == OperandType.Memory:
        cpu.memory.write(target_address, source_value)
    else:
        error("Unable to write to immediate")


def NOP(cpu, ins):
    pass


def EXC(cpu, ins):
    source_type = ins.source.type
    target_type = ins.target.type

    if source_type == OperandType.Number:
        error("Cannot have an immediate as a swapped object")

    source_value = get_value(cpu, ins.source)
    target_value = get_value(cpu, ins.target)

    if target_type == OperandType.Register:
        cpu.register.set(ins.target.value, source_value)
    elif target_type == OperandType.Memory:
        cpu.memory.write(ins.target.value, source_value)

    if target_value is not None:
        write_value(cpu, source_type, ins.source.value, target_value)


def ADD(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    # 获取目标操作数的值
    target_value = get_value(cpu, ins.target)

    # 执行加法操作
    result = target_value + source_value
    # 将结果写回到目标操作数
    write_value(cpu, ins.parameter.type, ins.parameter.value, result)


def SUB(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    # 获取目标操作数的值
    target_value = get_value(cpu, ins.target)

    # 执行加法操作
    result = target_value - source_value

    # 将结果写回到目标操作数
    write_value(cpu, ins.parameter.type, ins.parameter.value, result)


def MUL(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    # 获取目标操作数的值
    target_value = get_value(cpu, ins.target)

    # 执行加法操作
    result = target_value * source_value

    # 将结果写回到目标操作数
    write_value(cpu, ins.parameter.type, ins.parameter.value, result)


def MOD(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    # 获取目标操作数的值
    target_value = get_value(cpu, ins.target)

    # 执行加法操作
    result = target_value % source_value

    # 将结果写回到目标操作数
    write_value(cpu, ins.parameter.type, ins.parameter.value, result)


def PUSH(cpu, ins):
    source_value = get_value(cpu, ins.source)
    cpu.stack.push(source_value)


def POP(cpu, ins):
    s = cpu.stack.pop()
    write_value(cpu, ins.source.type, ins.source.value, s)


def AND(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    # 获取目标操作数的值
    target_value = get_value(cpu, ins.target)

    # 执行加法操作
    result = target_value & source_value

    # 将结果写回到目标操作数
    write_value(cpu, ins.parameter.type, ins.parameter.value, result)


def OR(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    # 获取目标操作数的值
    target_value = get_value(cpu, ins.target)

    # 执行加法操作
    result = target_value | source_value

    # 将结果写回到目标操作数
    write_value(cpu, ins.parameter.type, ins.parameter.value, result)


def NOT(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)

    # 执行加法操作
    result = ~source_value

    # 将结果写回到目标操作数
    write_value(cpu, ins.target.type, ins.target.value, result)


def XOR(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    # 获取目标操作数的值
    target_value = get_value(cpu, ins.target)

    # 执行加法操作
    result = target_value ^ source_value

    # 将结果写回到目标操作数
    write_value(cpu, ins.parameter.type, ins.parameter.value, result)


def SHL(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    # 获取目标操作数的值
    target_value = get_value(cpu, ins.target)

    # 执行加法操作
    result = target_value << source_value

    # 将结果写回到目标操作数
    write_value(cpu, ins.parameter.type, ins.parameter.value, result)


def SHR(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    # 获取目标操作数的值
    target_value = get_value(cpu, ins.target)

    # 执行加法操作
    result = target_value >> source_value

    # 将结果写回到目标操作数
    write_value(cpu, ins.parameter.type, ins.parameter.value, result)


def JMP(cpu, ins):
    # 获取源操作数的值
    source_value = get_value(cpu, ins.source)
    cpu.register.pc = source_value

def JNZ(cpu, ins):
    source_value = get_value(cpu, ins.source)
    if source_value != 0:
        cpu.register.pc = ins.target.value

def JZ(cpu, ins):
    source_value = get_value(cpu, ins.source)
    if source_value == 0:
        cpu.register.pc = ins.target.value

def JE(cpu, ins):
    source_value = get_value(cpu, ins.source)
    target_value = get_value(cpu, ins.target)
    address = get_value(cpu, ins.parameter)
    if source_value == target_value:
        cpu.register.pc = address

def JGE(cpu, ins):
    source_value = get_value(cpu, ins.source)
    target_value = get_value(cpu, ins.target)
    address = get_value(cpu, ins.parameter)
    if source_value >= target_value:
        cpu.register.pc = address

def JG(cpu, ins):
    source_value = get_value(cpu, ins.source)
    target_value = get_value(cpu, ins.target)
    address = get_value(cpu, ins.parameter)
    if source_value > target_value:
        cpu.register.pc = address

def JB(cpu, ins):
    source_value = get_value(cpu, ins.source)
    target_value = get_value(cpu, ins.target)
    address = get_value(cpu, ins.parameter)
    if source_value < target_value:
        cpu.register.pc = address

def JBE(cpu, ins):
    source_value = get_value(cpu, ins.source)
    target_value = get_value(cpu, ins.target)
    address = get_value(cpu, ins.parameter)
    if source_value <= target_value:
        cpu.register.pc = address

def JNE(cpu, ins):
    source_value = get_value(cpu, ins.source)
    target_value = get_value(cpu, ins.target)
    address = get_value(cpu, ins.parameter)
    if source_value != target_value:
        cpu.register.pc = address
