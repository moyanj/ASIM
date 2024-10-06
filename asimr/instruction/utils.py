from asimr.constant import OperandType

def get_value(cpu, operand):
    print(operand)
    if operand.type == OperandType.Number:
        return operand.value
    elif operand.type == OperandType.Register:
        return cpu.register.get(operand.value)
    elif operand.type == OperandType.Memory:
        return cpu.memory.read(operand.value)


def write_value(cpu, operand_type, address, data):
    print(operand_type, address, data)
    if operand_type == OperandType.Register:
        print(cpu.register)

        return cpu.register.set(address, data)
    elif operand_type == OperandType.Memory:
        
        print(cpu.memory)
        return cpu.memory.write(address, data)
        
    print(cpu.register)
