from asimr.device import Memory, Stack, Register
from asimr.constant import MemoryError, ASIMError
import pytest


def test_write_out_of_bounds():
    mem = Memory(8)
    with pytest.raises(MemoryError):
        mem.write(8, 12)  # 尝试写入超出内存大小的地址


def test_read_out_of_bounds():
    mem = Memory(8)
    with pytest.raises(MemoryError):
        mem.read(8)  # 尝试读取超出内存大小的地址


def test_write_negative_address():
    mem = Memory(8)
    with pytest.raises(MemoryError):
        mem.write(-1, 12)  # 尝试写入负地址


def test_read_negative_address():
    mem = Memory(8)
    with pytest.raises(MemoryError):
        mem.read(-1)  # 尝试读取负地址


def test_read_zero_address():
    mem = Memory(8)
    mem.write(0x0, 46)
    r = mem.read(0x0)
    assert r == 46


def test_write_max_value():
    mem = Memory(8)
    mem.write(0x0, 255)  # 测试写入最大值（对于8位设备）
    assert mem.data[0] == 255


def test_write_min_value():
    mem = Memory(8)
    mem.write(0x0, 0)  # 测试写入最小值
    assert mem.data[0] == 0


def test_stack_push_pop():
    stack = Stack()
    stack.push(10)
    stack.push(20)
    assert stack.pop() == 20
    assert stack.pop() == 10


def test_stack_overflow():
    stack = Stack(size=1)
    stack.push(10)
    with pytest.raises(ASIMError):
        stack.push(20)  # 尝试在满栈上推入元素


def test_stack_underflow():
    stack = Stack()
    assert stack.pop() == 0  # 尝试在空栈上弹出元素


def test_initial_state():
    reg = Register()
    assert reg.pc == 0
    assert reg.sr == 0
    assert reg.tc == 0
    for val in reg._GPR:
        assert val == 0


def test_set_get_register():
    reg = Register()
    reg.set(0, 0x12)
    assert reg.get(0) == 0x12


def test_out_of_range_register_set():
    reg = Register()
    with pytest.raises(ASIMError):
        reg.set(32, 0x12345678)  # 尝试设置一个不存在的寄存器


def test_out_of_range_register_get():
    reg = Register()
    with pytest.raises(ASIMError):
        reg.get(32)  # 尝试获取一个不存在的寄存器
