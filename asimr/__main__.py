import argparse
import pickle
import zstandard
from asimr.core import Core, Instruction
from asimr.device import Register, Memory, Stack
from asimr.constant import Program


def run(file):
    with open(file, "rb") as f:
        data = f.read()
        data = zstandard.decompress(data[4:])
        obj: Program = pickle.loads(data)

    register = Register(obj.n_GPR)
    data_mem = Memory(obj.data_mem)
    inst_mem = Memory(obj.inst_mem, strict=False)
    stack = Stack(obj.stack_size)

    cpu = Core(register, data_mem, inst_mem, stack)
    for i, inst in enumerate(obj.instructions):
        cpu.instruction_memory.write(i, inst)
    cpu.run()


def main():
    parser = argparse.ArgumentParser(description="Run an assembly file.")
    parser.add_argument("file", type=str, help="The path to the assembly file to run.")
    args = parser.parse_args()
    run(args.file)


if __name__ == "__main__":
    main()
