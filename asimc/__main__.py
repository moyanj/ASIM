import argparse
import os
import pickle
import sys
import zstandard
import jinja2
from asimc.log import logger
from asimc.parser import Parser
from asimc.funcs import funcs
from asimr.constant import tmp


def asm(file, output_file, pretend, include_dir=None, worker=1, level=5):
    if output_file is None and pretend:
        output_file = os.path.splitext(file)[0] + ".acp"
    else:
        output_file = output_file or os.path.splitext(file)[0] + ".acb"

    logger.info("Start Compile...")

    if not os.path.exists(file) and not os.path.isfile(file):
        logger.error("File does not exist.")
        sys.exit()

    logger.info(f"Input file: {file}")
    logger.info(f"Output file: {output_file}")
    logger.info(f"processes: {worker}")
    logger.info(f"Compression level：{level}")

    logger.info("Preprocessing..")
    tmp["inc_dir"] = ["."] + include_dir

    env = jinja2.Environment(
        loader=jinja2.DictLoader({os.path.basename(file): open(file).read()}),
        variable_start_string="{",
        variable_end_string="}",
        block_start_string="%",
        block_end_string="%",
    )

    f_t = env.get_template(os.path.basename(file))

    if pretend:
        with open(output_file, "w") as of:
            of.write(f_t.render(**funcs))
        logger.success("Done.")
        return

    logger.info("Parsing...")
    p = Parser(f_t.render(**funcs), worker)
    p.parser()
    logger.info("Saving...")
    data = pickle.dumps(p.out)
    data = zstandard.compress(data, level=level)

    with open(output_file, "wb") as of:
        of.write(b"zstd" + data)
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
        "-p", "--pretend", action="store_true", help="Only perform preprocessing."
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
    args = parser.parse_args()
    asm(args.file, args.output, args.pretend, args.include_dir, args.jobs, args.level)


if __name__ == "__main__":
    main()
