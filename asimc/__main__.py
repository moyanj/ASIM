import argparse
import os
import pickle
import sys
import zstandard
import jinja2
import tempfile
from asimc.log import logger
from asimc.parser import Parser
from asimc.funcs import funcs
from asimc.translator import CppTranslator
from asimr.constant import tmp, __version__

def make_name(file, tp, compile):
    if tp == 'acb':
        return os.path.splitext(file)[0] + ".acb"
    elif tp == 'acp':
        return os.path.splitext(file)[0] + ".acp"
    elif tp == 'cpp':
        if compile:
            return os.path.splitext(file)[0] + ".out"
            
        else:
            return os.path.splitext(file)[0] + ".cpp"
            
    else:
        raise ValueError(f'Unknown type: {tp}')

def out_acb(p, output_file, level):
    logger.info("Saving...")
    # 保存并压缩
    data = pickle.dumps(p.out)
    data = zstandard.compress(data, level=level)

    with open(output_file, "wb") as of:
        of.write(b"zstd" + data)
    
    
def asm(file, output_file, include_dir, worker, level, tp, compile, use_gcc, use_clang):
    
    # 生成文件名
    if output_file is None:
        output_file = make_name(file, tp, compile)
        
    logger.info(f"ASIM Compiler v{__version__}")
    logger.info("Start Compiling...")
    
    # 判断源文件是否存在
    if not os.path.exists(file) and not os.path.isfile(file):
        logger.error("File does not exist.")
        sys.exit()

    logger.info(f"Processes: {worker}")
    logger.info(f"Compression level：{level}")
    logger.info("Preprocessing..")
    
    # jinja2渲染
    tmp["inc_dir"] = ["."] + include_dir

    env = jinja2.Environment(
        loader=jinja2.DictLoader({os.path.basename(file): open(file).read()}),
        variable_start_string="{",
        variable_end_string="}",
        block_start_string="%",
        block_end_string="%",
    )

    f_t = env.get_template(os.path.basename(file))

    if tp == 'acp':
        with open(output_file, "w") as of:
            of.write(f_t.render(**funcs))
        logger.success("Done.")
        return
    
    # 解析
    logger.info("Parsing...")

    p = Parser(f_t.render(**funcs), worker)
    p.parser()
    
    if tp == 'acb':
        out_acb(p, output_file, level)
    elif tp == 'cpp':
        t = CppTranslator(p.out, compile, use_gcc, use_clang)
        open(os.path.join(tempfile.gettempdir(),'asim_temp.cpp'), 'w').write(t.render())
        t.tran(os.path.join(tempfile.gettempdir(),'asim_temp.cpp'), output_file, compile)        
    
    logger.success("Done.")


def main():
    parser = argparse.ArgumentParser(description="Compile an assembly file.")

    parser.add_argument(
        "file", type=str, help="The path to the assembly file to compile."
    )
    
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="The path to the output file.",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        help="Number of threads compiled in parallel.",
    )
    
    parser.add_argument(
        "-i",
        "--include_dir",
        type=str,
        nargs="*",
        default=[],
        help="Directories to include for template lookup.",
    )
    parser.add_argument(
        "-l",
        "--level",
        type=int,
        default=5,
        help="Compression level",
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        default='asb',
        help='Output format'
    )
    parser.add_argument("-c", '--compile', action="store_true", help="Use GCC for compilation.")
    parser.add_argument("--use-gcc", action="store_true", help="Use GCC for compilation.")
    parser.add_argument("--use-clang", action="store_true", help="Use Clang for compilation.")
    
    args = parser.parse_args()
    asm(
        args.file,
        args.output,
        args.include_dir,
        args.jobs,
        args.level,
        args.type,
        args.compile,
        args.use_gcc,
        args.use_clang
    )


if __name__ == "__main__":
    main()
