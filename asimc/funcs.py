import os
import base64
from asimr.constant import tmp, SyscallTable


def str2list(text: str):
    return [ord(c) for c in text]


def crange(*args, **kwargs):
    for i in range(*args, **kwargs):
        yield hex(i)


def cenumerate(*args, **kwargs):
    for i, v in enumerate(*args, **kwargs):
        yield hex(i), v


def include(file_name: str):

    inc_dirs = tmp["inc_dir"]
    file_path = None

    for d in inc_dirs:
        # 检查文件是否以特定的扩展名结尾
        if file_name.endswith((".ac", ".acb", ".acp")):
            full_names = [file_name]
        else:
            full_names = [file_name] + [
                file_name + ext for ext in [".ac", ".acb", ".acp"]
            ]

        for f in full_names:
            file_path = os.path.join(d, f)
            if os.path.exists(file_path):
                break

    if file_path is None:
        raise FileNotFoundError(f"Cannot find file: {file_name}")

    with open(file_path, "rb") as f:
        magic_number = f.read(4).decode()
        f.seek(0)
        if magic_number == "zstd":
            return f".include_zstd {file_path} {base64.b85encode(f.read()).decode()}\n"
        else:
            return f".include_file {file_path}\n{f.read().decode()}\n;! end_include {file_path}"

    return ""  # 如果没有找到文件，返回 None 或其他适当的值


funcs = {
    "str2list": str2list,
    "range": crange,
    "rrange": range,
    "enumerate": cenumerate,
    "renumerate": enumerate,
    "include": include,
    "syscall": SyscallTable,
}
