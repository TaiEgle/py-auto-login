# 快速开始指南

## 本地启动项目

### 前置要求

1. **Python 3.10+**
   ```bash
   python --version
   ```

2. **pip**（Python 包管理器）

### 步骤 1：安装依赖

```bash
# 进入项目目录
cd py-auto-login

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 步骤 2：配置账号密码

首次运行会自动生成 `config.json` 文件，也可以手动创建：

```json
{
  "username": "你的账号",
  "password": "你的密码",
  "slow_mo": 50
}
```

### 步骤 3：运行程序

```bash
python main.py
```

## 常见问题

### Q1: 提示 "Playwright 未安装"
```bash
pip install playwright
playwright install chromium
```

### Q2: 提示 "找不到浏览器"
程序会自动按以下优先级查找浏览器：
1. 打包的浏览器（browser/chromium/）
2. Playwright 下载的浏览器
3. 系统安装的 Chrome

如果都没找到，请安装 Chrome 浏览器或运行：
```bash
playwright install chromium
```

### Q3: 程序运行后卡住
- 检查网络连接
- 检查账号密码是否正确
- 查看 `error.log` 文件获取详细错误信息

## 开发模式

### 安装开发依赖（可选）
```bash
pip install -r requirements.txt
```

### 调试模式
直接运行 `python main.py`，所有日志会输出到控制台。

## 打包成 EXE（Windows）

### 方法 1：使用 build.py（推荐）
```bash
python build.py
```

### 方法 2：手动使用 PyInstaller
```bash
pip install pyinstaller
pyinstaller --name=auto-login --onefile --console main.py
```

打包后的 exe 文件会在 `dist/` 目录中。
