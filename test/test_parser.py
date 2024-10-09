from asimc.cache import LRUCache
from asimc.parser import Parser, CodeParser
import asimc.funcs as asim_f
from asimr.constant import tmp, InstructionSet
from asimr.core import Instruction
import pytest


def test_cache_null_ret():
    c = LRUCache(1)
    d = c.get("aaa")
    assert d == -1


def test_cache():
    c = LRUCache(1)
    c.put("ddd", 1)
    r = c.get("ddd")
    assert r == 1


def test_cache_overflow():
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    r = c.get(1)
    r2 = c.get(2)
    assert r == -1
    assert r2 == 2


# 测试 include 函数当文件存在时的行为
def test_include_file_exists(mocker):
    mocker.patch("os.path.exists", return_value=True)
    f = mocker.mock_open(read_data=b"114514")
    mocker.patch("builtins.open", f)
    tmp["inc_dir"] = ["."]
    r = asim_f.include("a.ac")
    ret = ".include_file ./a.ac\n14\n;! end_include ./a.ac"
    assert r == ret


# 测试 include 函数当文件不存在时的行为
def test_include_file_not_found(mocker):
    mocker.patch("os.path.exists", return_value=False)
    tmp["inc_dir"] = ["."]
    with pytest.raises(FileNotFoundError):
        asim_f.include("non_existent_file.ac")


# 测试 include 函数当文件是 zstd 压缩时的行为
def test_include_zstd_file(mocker):
    mocker.patch("os.path.exists", return_value=True)
    f = mocker.mock_open(read_data=b"zstd114514")
    mocker.patch("builtins.open", f)
    mocker.patch("base64.b85encode", return_value=b"encoded_content")
    result = asim_f.include("zstd_file.ac")
    assert ".include_zstd" in result
    assert "encoded_content" in result


def test_config_inst():
    p = CodeParser()
    code = """
.data_mem 114514
.inst_mem 114514
.n_GPR 32
.stack_size 128
""".split(
        "\n"
    )
    p.parser(code)
    out = p.out
    assert out.data_mem == 114514
    assert out.inst_mem == 114514
    assert out.n_GPR == 32
    assert out.stack_size == 128


def test_comment():
    code = "MOV 1 1 r_1 ; vvvv \n;sss"
    p = CodeParser()
    p.parser(code.split("\n"))
    out = Instruction.unpack(p.out.instructions[0])
    assert out.opcode == InstructionSet.MOV


def test_inst():
    code = ["MOV 1 r_1"]
    p = CodeParser()
    p.parser(code)
    out = Instruction.unpack(p.out.instructions[0])
    assert out.opcode == InstructionSet.MOV
    assert out.source.value == 1
    assert out.target.value == 1


# 运行测试
if __name__ == "__main__":
    pytest.main()
