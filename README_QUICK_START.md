# 快速开始指南（macOS 用户）

## ⚠️ 重要提示

在 macOS 上，Python 和 pip 的命令通常是：
- `python3` 而不是 `python`
- `pip3` 而不是 `pip`

如果 `pip` 命令找不到，请使用 `pip3` 或 `python3 -m pip`。

## 🚀 快速安装（推荐）

运行自动安装脚本：

```bash
chmod +x install.sh
./install.sh
```

这个脚本会自动：
- ✅ 检测 Python 环境
- ✅ 安装所有依赖
- ✅ 安装 Playwright 浏览器

## 📝 手动安装步骤

### 1. 安装 Python 依赖

```bash
# 方法 1：使用 pip3（推荐）
pip3 install -r requirements.txt

# 方法 2：使用 python3 -m pip
python3 -m pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
python3 -m playwright install chromium
python3 -m playwright install-deps chromium
```

### 3. 安装 Tesseract OCR

```bash
# macOS
brew install tesseract

# 验证安装
tesseract --version
```

### 4. 配置账号密码

```bash
# 如果配置文件不存在，复制示例
cp config.json.example config.json

# 编辑配置文件
nano config.json
# 或使用其他编辑器
```

填写账号密码：
```json
{
  "username": "你的账号",
  "password": "你的密码"
}
```

### 5. 运行程序

```bash
python3 main.py
```

## 🔧 常见问题

### Q: `pip: command not found`

**解决方案：**
```bash
# 使用 pip3
pip3 install -r requirements.txt

# 或使用 python3 -m pip
python3 -m pip install -r requirements.txt
```

### Q: `python: command not found`

**解决方案：**
```bash
# 使用 python3
python3 main.py

# 或创建别名（添加到 ~/.zshrc 或 ~/.bashrc）
alias python=python3
alias pip=pip3
```

### Q: 如何创建别名？

编辑你的 shell 配置文件：

```bash
# 对于 zsh（macOS 默认）
nano ~/.zshrc

# 添加以下行
alias python=python3
alias pip=pip3

# 保存后重新加载
source ~/.zshrc
```

### Q: 依赖安装失败

**解决方案：**
```bash
# 1. 更新 pip
python3 -m pip install --upgrade pip

# 2. 使用国内镜像源（如果网络慢）
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 或逐个安装
pip3 install playwright
pip3 install Pillow
pip3 install pytesseract
pip3 install psutil
```

## 📋 安装检查清单

运行前确保：

```bash
# 检查 Python
python3 --version  # 应该显示 Python 3.8+

# 检查 pip
pip3 --version  # 或 python3 -m pip --version

# 检查依赖
python3 -m pip list | grep -E "playwright|pytesseract|Pillow"

# 检查 Tesseract
tesseract --version

# 检查配置文件
cat config.json
```

## 🎯 测试组件

```bash
# 测试 OCR 引擎
python3 test_ocr.py

# 测试浏览器
python3 test_browser.py
```

## 📚 更多信息

- 详细文档：查看 [LOCAL_DEBUG.md](LOCAL_DEBUG.md)
- 优化说明：查看 [OPTIMIZATION.md](OPTIMIZATION.md)
- 完整文档：查看 [README.md](README.md)
