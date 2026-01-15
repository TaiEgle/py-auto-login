# 快速开始指南

## 1. 安装依赖

### Python 包
```bash
pip install -r requirements.txt
```

### Playwright 浏览器
```bash
playwright install chromium
```

### Tesseract OCR

**Windows:**
- 下载并安装 [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- 安装时选择添加到 PATH

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

## 2. 配置账号密码

首次运行会自动生成 `config.json` 文件：

```json
{
  "username": "你的账号",
  "password": "你的密码"
}
```

## 3. 运行程序

```bash
python main.py
```

## 4. 打包为可执行文件（可选）

### 本地打包
```bash
python build.py
```

### GitHub Actions 自动构建

推送到 GitHub 并创建标签时会自动构建：

```bash
git tag v1.0.0
git push origin v1.0.0
```

构建产物会自动发布到 GitHub Releases。

## 功能说明

- ✅ **自动识别验证码**：使用 Tesseract OCR 识别登录验证码
- ✅ **自动登录**：自动填写账号密码并提交
- ✅ **单实例运行**：防止多个实例同时运行
- ✅ **错误日志**：所有错误记录到 `error.log`
- ✅ **跨平台支持**：Windows / macOS / Linux
- ✅ **浏览器自动检测**：优先使用打包浏览器，其次 Playwright，最后系统 Chrome

## 故障排除

### 浏览器启动失败
1. 确保已安装 Playwright 浏览器：`playwright install chromium`
2. 检查浏览器路径配置
3. Windows 可能需要安装 Visual C++ Redistributable

### OCR 识别失败
1. 确保已安装 Tesseract OCR
2. 检查 `lang-data` 目录是否存在（可选）
3. 检查环境变量配置

### 锁文件错误
- 手动删除 `python-auto-login.lock` 文件
- 或结束相关进程
