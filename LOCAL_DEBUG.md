# 本地调试运行指南

## 快速开始

### 1. 安装 Python 依赖

```bash
# 安装核心依赖（推荐）
pip3 install -r requirements.txt

# 或者只安装必需的（最小化）
pip3 install playwright Pillow pytesseract psutil

# 注意：macOS 上通常使用 pip3，如果 pip3 不行，使用：
python3 -m pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
# 安装 Chromium 浏览器
playwright install chromium

# 安装浏览器依赖（系统级）
playwright install-deps chromium
```

### 3. 安装 Tesseract OCR

#### macOS
```bash
# 使用 Homebrew
brew install tesseract

# 验证安装
tesseract --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr

# 验证安装
tesseract --version
```

#### Windows
1. 下载安装包：https://github.com/UB-Mannheim/tesseract/wiki
2. 安装时选择添加到 PATH
3. 或者在 PowerShell 中验证：
   ```powershell
   tesseract --version
   ```

### 4. 创建配置文件

```bash
# 复制示例配置文件
cp config.json.example config.json

# 编辑配置文件
# macOS/Linux
nano config.json
# 或
vim config.json

# Windows
notepad config.json
```

编辑 `config.json`，填写你的账号密码：

```json
{
  "username": "你的账号",
  "password": "你的密码",
  "headless": false,
  "ocr_engine": "auto",
  "max_retries": 10,
  "slow_mo": 50
}
```

### 5. 运行程序

```bash
# 直接运行
python main.py

# 或使用 Python 3
python3 main.py
```

## 调试技巧

### 1. 启用详细日志

修改 `main.py` 或在代码中添加调试信息：

```python
import logging

# 在 main() 函数开头添加
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 2. 使用无头模式调试（可选）

在 `config.json` 中设置：

```json
{
  "headless": true,
  "slow_mo": 100
}
```

### 3. 测试 OCR 引擎

创建测试脚本 `test_ocr.py`：

```python
#!/usr/bin/env python3
from ocr_engine import get_available_engines, create_ocr_engine
from pathlib import Path

# 检查可用引擎
engines = get_available_engines()
print("可用的 OCR 引擎:")
for engine_type, description in engines:
    print(f"  - {description}")

# 测试 Tesseract
try:
    ocr = create_ocr_engine('tesseract')
    print("\n✅ Tesseract 可用")
except Exception as e:
    print(f"\n❌ Tesseract 不可用: {e}")
```

运行：
```bash
python test_ocr.py
```

### 4. 测试浏览器启动

创建测试脚本 `test_browser.py`：

```python
#!/usr/bin/env python3
from browser_manager import BrowserManager

try:
    with BrowserManager(headless=False, slow_mo=100) as bm:
        page = bm.page
        page.goto("https://www.example.com")
        print("✅ 浏览器启动成功")
        input("按 Enter 键关闭浏览器...")
except Exception as e:
    print(f"❌ 浏览器启动失败: {e}")
    import traceback
    traceback.print_exc()
```

运行：
```bash
python test_browser.py
```

### 5. 常见问题排查

#### 问题 1: Playwright 浏览器未找到

```bash
# 检查浏览器安装位置
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); print(p.chromium.executable_path); p.stop()"
```

#### 问题 2: Tesseract 未找到

```bash
# 检查 Tesseract 路径（macOS）
which tesseract

# 检查 Tesseract 路径（Linux）
which tesseract

# Windows 检查
tesseract --version
```

如果路径不对，可以在代码中手动设置：

```python
# 在 main.py 的 get_tesseract_cmd() 中添加自定义路径
# 或者在 config.json 中配置
```

#### 问题 3: 模块导入错误

```bash
# 检查 Python 环境
python3 -m pip list | grep -E "playwright|pytesseract|Pillow"

# 如果缺失，重新安装
pip3 install playwright pytesseract Pillow psutil
# 或
python3 -m pip install playwright pytesseract Pillow psutil
```

#### 问题 4: 验证码识别失败

- 检查 OCR 引擎是否正常：运行 `test_ocr.py`
- 尝试切换 OCR 引擎（Tesseract ↔ EasyOCR）
- 检查图片质量（保存验证码图片查看）

### 6. 调试模式运行

修改 `main.py`，在关键位置添加调试输出：

```python
# 在 wait_for_captcha_image() 函数中添加
print(f"[DEBUG] 验证码 Base64 长度: {len(base64_string)}")

# 在 OCR 识别后添加
print(f"[DEBUG] OCR 原始结果: {captcha_result}")
print(f"[DEBUG] OCR 处理后: {captcha_result.strip().replace(' ', '')}")
```

### 7. 保存验证码图片（调试用）

在 `main.py` 的 OCR 识别部分添加：

```python
# 保存验证码图片用于调试
with open(f"captcha_{int(time.time())}.png", "wb") as f:
    f.write(image_data)
print(f"[DEBUG] 验证码图片已保存")
```

### 8. 使用 IDE 调试

#### VS Code

1. 创建 `.vscode/launch.json`：
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: 当前文件",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: main.py",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

2. 设置断点，按 F5 启动调试

#### PyCharm

1. 右键点击 `main.py`
2. 选择 "Debug 'main'"
3. 设置断点进行调试

## 完整调试流程示例

```bash
# 1. 检查环境
python --version
pip --version

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装浏览器
playwright install chromium

# 4. 检查 OCR
tesseract --version

# 5. 创建配置
cp config.json.example config.json
# 编辑 config.json，填写账号密码

# 6. 测试各组件
python test_ocr.py      # 测试 OCR
python test_browser.py  # 测试浏览器

# 7. 运行主程序
python main.py

# 8. 查看日志
cat error.log  # 如果有错误
```

## 开发模式建议

### 1. 使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 代码格式化

```bash
# 安装格式化工具
pip install black isort

# 格式化代码
black *.py
isort *.py
```

### 3. 代码检查

```bash
# 安装检查工具
pip install flake8 pylint

# 检查代码
flake8 *.py
pylint *.py
```

## 快速检查清单

运行前确保：

- [ ] Python 3.8+ 已安装
- [ ] 所有依赖已安装：`pip install -r requirements.txt`
- [ ] Playwright 浏览器已安装：`playwright install chromium`
- [ ] Tesseract OCR 已安装并可用：`tesseract --version`
- [ ] 配置文件已创建：`config.json` 存在且填写了账号密码
- [ ] 网络连接正常（能访问登录页面）

## 遇到问题时

1. 查看 `error.log` 文件
2. 运行测试脚本检查组件
3. 查看终端输出的错误信息
4. 检查配置文件格式是否正确
5. 确认所有依赖都已正确安装

## 下一步

- 阅读 [README.md](README.md) 了解完整功能
- 查看 [OPTIMIZATION.md](OPTIMIZATION.md) 了解优化详情
- 参考 [QUICKSTART.md](QUICKSTART.md) 快速入门
