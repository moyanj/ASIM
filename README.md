# ASIM

ASIM是一款编程语言，它以一个高性能CPU模拟器为基础，提供了强大的脚本编写能力。

## 安装指南

### 使用Pypi

```bash
pip install asim
```

### 使用Debian源

```bash
sudo apt install curl
curl https://source.moyanjdc.top/deb/install.sh | bash
sudo apt install asim
```

### Github仓库

参见[从源码运行](dev/)

## 快速开始
将以下代码写入`t.ac`

```
% for i, v in str2list("Hello World!"): %
PAC {i}
% endfor %
```
使用`asimc`编译代码：

```bash
asimc t.ac -o t.acb
```
使用`asimr`运行代码：

```bash
asimr t.acb
```

运行以上代码，你将看到屏幕上打印出“Hello World!”。
