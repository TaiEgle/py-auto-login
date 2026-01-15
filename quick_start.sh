#!/bin/bash
# 快速启动脚本（macOS/Linux）

echo "=========================================="
echo "Python 自动登录 - 快速启动"
echo "=========================================="
echo ""

# 检查 Python
echo "1. 检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "   ✅ 找到 Python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "   ✅ 找到 Python"
else
    echo "   ❌ 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

# 检查依赖
echo ""
echo "2. 检查依赖..."
if ! $PYTHON_CMD -c "import playwright" 2>/dev/null; then
    echo "   ⚠️  Playwright 未安装，正在安装..."
    $PYTHON_CMD -m pip install playwright 2>&1 | grep -v "WARNING" || true
    echo "   ✅ Playwright 安装完成"
else
    echo "   ✅ Playwright 已安装"
fi

if ! $PYTHON_CMD -c "import pytesseract" 2>/dev/null; then
    echo "   ⚠️  pytesseract 未安装，正在安装..."
    $PYTHON_CMD -m pip install pytesseract Pillow 2>&1 | grep -v "WARNING" || true
    echo "   ✅ pytesseract 安装完成"
else
    echo "   ✅ pytesseract 已安装"
fi

# 检查浏览器
echo ""
echo "3. 检查浏览器..."
if ! $PYTHON_CMD -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); p.chromium.executable_path; p.stop()" 2>/dev/null | grep -q chromium; then
    echo "   ⚠️  Playwright 浏览器未安装，正在安装..."
    $PYTHON_CMD -m playwright install chromium
    echo "   ✅ 浏览器安装完成"
else
    echo "   ✅ 浏览器已安装"
fi

# 检查 Tesseract
echo ""
echo "4. 检查 Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version 2>&1 | head -n 1)
    echo "   ✅ Tesseract 已安装: $TESSERACT_VERSION"
else
    echo "   ⚠️  Tesseract 未安装"
    echo "   请安装 Tesseract:"
    echo "   macOS: brew install tesseract"
    echo "   Ubuntu: sudo apt-get install tesseract-ocr"
    echo "   或在 Windows 下载安装包"
fi

# 检查配置文件
echo ""
echo "5. 检查配置文件..."
if [ ! -f "config.json" ]; then
    echo "   ⚠️  配置文件不存在，正在创建..."
    cp config.json.example config.json 2>/dev/null || cat > config.json << EOF
{
  "username": "你的账号",
  "password": "你的密码"
}
EOF
    echo "   ✅ 配置文件已创建"
    echo "   ⚠️  请编辑 config.json 填写账号密码！"
else
    echo "   ✅ 配置文件存在"
fi

echo ""
echo "=========================================="
echo "准备完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 编辑 config.json 填写账号密码"
echo "2. 运行程序: $PYTHON_CMD main.py"
echo "3. 或运行测试: $PYTHON_CMD test_ocr.py"
echo ""
