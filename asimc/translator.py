import subprocess
from asimr.constant import Program
from asimr.core import Instruction
from jinja2 import Environment, FileSystemLoader
import os

def run_command(command):
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8')

class CppTranslator:
    def __init__(self, p:Program, compile, use_gcc=False, use_clang=False):
        self.p = p
        self.c = compile
        self.compile = self.find_compile(use_gcc, use_clang)
        self.items = []
        
    def find_compile(self, use_gcc, use_clang):
        # 尝试使用指定的编译器
        if use_gcc:
            return 'g++'
        elif use_clang:
            return 'clang++'
        
        # 如果没有指定编译器，尝试检测系统中的编译器
        try:
            run_command('g++ --version')
            return 'g++'
        except subprocess.CalledProcessError:
            pass
        
        try:
            run_command('clang++ --version')
            return 'clang++'
        except subprocess.CalledProcessError:
            pass
        
        # 如果没有找到编译器，抛出异常
        raise Exception("No suitable compiler found.")

    
    def render(self):
        for inst in self.p.instructions:
            inst = Instruction.unpack(inst)
            
            name = inst.opcode.name
            if hasattr(self, 'inst_'+name):
                func = getattr(self, 'inst_'+name)
                func(inst)
            else:
                raise TypeError('Unsupported instruction')
                
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'cpp')))
        
        tp = env.get_template('main.cpp')
        return tp.render(data_mem=self.p.data_mem, stack_size=self.p.stack_size, n_GPR=self.p.n_GPR, items=self.items)
        