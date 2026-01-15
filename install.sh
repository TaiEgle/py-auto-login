#!/bin/bash
# 安装脚本 - 自动安装所有依赖

echo "=========================================="
echo "Python 自动登录 - 依赖安装"
echo "=========================================="
echo ""

# 检测 Python 命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

echo "使用 Python: $($PYTHON_CMD --version)"
echo ""

# 检查 pip
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    echo "✅ 找到 pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    echo "✅ 找到 pip"
elif $PYTHON_CMD -m pip --version &> /dev/null; then
    PIP_CMD="$PYTHON_CMD -m pip"
    echo "✅ 使用 python3 -m pip"
else
    echo "❌ 未找到 pip，正在安装..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $PYTHON_CMD get-pip.py
    rm get-pip.py
    PIP_CMD="$PYTHON_CMD -m pip"
fi

echo ""
echo "使用 pip: $PIP_CMD"
echo ""

# 安装依赖
echo "正在安装 Python 依赖..."
$PIP_CMD install --upgrade pip 2>&1 | grep -v "WARNING" || true

echo ""
echo "正在安装项目依赖..."
$PIP_CMD install -r requirements.txt 2>&1 | grep -v "WARNING" || true

echo ""
echo "正在安装 Playwright 浏览器..."
$PYTHON_CMD -m playwright install chromium 2>&1 | grep -v "WARNING" || true

echo ""
echo "=========================================="
echo "✅ 依赖安装完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 编辑 config.json 填写账号密码"
echo "2. 运行: $PYTHON_CMD main.py"
echo ""
