#ifndef ASIM_H
#define ASIM_H
#include <iostream>
#include <vector>
#include <stdexcept>
#include <string>

// 使用模板定义一个带最大容量限制的栈
template <typename T>
class Stack {
private:
    std::vector<T> data;      // 存储栈中元素的动态数组
    size_t maxSize;          // 栈的最大容量

public:
    // 构造函数，初始化最大容量
    Stack(size_t maxSize) : maxSize(maxSize) {}

    // 入栈操作，如果栈已满则抛出异常
    void push(const T& value) {
        if (data.size() >= maxSize) {
            throw std::overflow_error("Stack overflow");
        }
        data.push_back(value);
    }

    // 出栈操作，如果栈为空则抛出异常
    void pop() {
        if (data.empty()) {
            throw std::underflow_error("Stack underflow");
        }
        data.pop_back();
    }

    // 获取栈顶元素的引用，如果栈为空则抛出异常
    T& top() {
        if (data.empty()) {
            throw std::underflow_error("Stack underflow");
        }
        return data.back();
    }

    // 检查栈是否为空
    bool empty() const {
        return data.empty();
    }

    // 获取栈中元素的数量
    size_t size() const {
        return data.size();
    }
};

// 定义一个结构体来模拟寄存器
struct Register {
    unsigned short gpr[16];  // 通用寄存器数组
    unsigned int pc = 0;      // 程序计数器
    unsigned int sr = 0;      // 状态寄存器
    unsigned int tc = 0;      // 时间计数器

    // 构造函数，初始化寄存器的值
    Register() : pc(0), sr(0), tc(0) {
        for (auto& reg : gpr) {
            reg = 0;
        }
    }
};

// 全局寄存器实例
Register asim_reg;

// 模拟数据内存的全局数组
unsigned short asim_mem[8 * 1024 * 1024];

// 创建一个大小为128的栈实例
Stack<short> asim_stack(128);

#endif
