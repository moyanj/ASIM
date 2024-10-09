#include "asim.hpp"
#include <iostream>

// 模拟数据内存的全局数组
unsigned short asim_mem[{{ data_mem }}];

// 创建一个大小为128的栈实例
Stack<short> asim_stack({{ stack_size }});

// 全局寄存器实例
Register asim_reg({{ n_GPR }});

using namespace std;

int main() {

{% for index, item in enumerate(items) %}
    line_{{ index }}:
    {{ item }}
{% endfor %}

}