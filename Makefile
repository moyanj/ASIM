POETRY = poetry

# 默认目标
all: build

# 安装项目依赖
install:
	$(POETRY) install

# 构建项目包
build: test
	$(POETRY) build

# 清理项目，删除构建文件和缓存
clean:
	rm -rf dist .pytest_cache report.html
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.build' -exec rm -rf {} +
	find . -name '*.dist' -exec rm -rf {} +
	find . -name '*.onefile-build' -exec rm -rf {} +
	find . -name '*.acb' -exec rm -rf {} +

# 格式化代码
format: 
	$(POETRY) run black .

# 运行测试
test: format
	$(POETRY) run pytest --html=report.html --self-contained-html test