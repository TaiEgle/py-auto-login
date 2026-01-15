# Python 自动登录脚本

基于 Playwright 和 Tesseract OCR 的自动登录工具。

## 功能特性

- ✅ 自动识别验证码并登录
- ✅ 单实例运行（防止多个实例同时启动）
- ✅ 错误日志记录
- ✅ 跨平台支持（Windows / macOS / Linux）
- ✅ 支持打包为可执行文件
- ✅ 自动浏览器路径检测（打包浏览器 > Playwright > 系统 Chrome）
- ✅ **支持多种 OCR 引擎**（Tesseract 轻量级 / EasyOCR 高准确率）
- ✅ **支持无头模式**（减少资源占用）
- ✅ **模块化设计**（易于维护和扩展）
- ✅ **体积优化**（打包体积减少 25%）

## 环境要求

### 1. Python 环境

- Python 3.8 或更高版本

### 2. 系统依赖

#### Tesseract OCR

**Windows:**
1. 下载安装 [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
2. 安装时选择将 Tesseract 添加到 PATH
3. 或者手动设置环境变量 `TESSDATA_PREFIX`

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install tesseract
```

### 3. Python 依赖

```bash
pip install -r requirements.txt
```

### 4. Playwright 浏览器

安装 Chromium 浏览器：

```bash
playwright install chromium
```

如果需要使用中文验证码识别，还需要下载中文语言数据包。

## 使用方法

### 1. 配置账号密码

首次运行会在当前目录生成 `config.json` 文件：

```json
{
  "username": "你的账号",
  "password": "你的密码"
}
```

填写你的账号和密码后重新运行程序。

### 2. 配置选项（可选）

编辑 `config.json` 可配置更多选项：

```json
{
  "username": "你的账号",
  "password": "你的密码",
  "headless": false,      // 是否使用无头模式（减少资源占用）
  "ocr_engine": "auto",   // OCR 引擎: auto/tesseract/easyocr
  "max_retries": 10,      // 最大重试次数
  "slow_mo": 50           // 操作延迟（毫秒）
}
```

### 3. 运行程序

```bash
python main.py
```

### 3. 打包为可执行文件（可选）

使用 PyInstaller 打包：

```bash
python build.py
```

打包后的可执行文件在 `dist` 目录中。

**注意：**
- 打包后的程序仍然需要 Tesseract OCR
- 如果需要包含浏览器，需要将 Playwright 下载的浏览器复制到 `browser/chromium/` 目录
- 如果需要 OCR 语言数据，将 `lang-data` 目录放在程序同目录

## 项目结构

```
py-auto-login/
├── main.py              # 主程序
├── requirements.txt     # Python 依赖
├── build.py            # 本地打包脚本
├── .github/
│   └── workflows/
│       └── build.yml   # GitHub Actions 构建配置
├── config.json         # 配置文件（需自行创建）
├── lang-data/          # Tesseract 语言数据（可选）
└── browser/            # 打包的浏览器（可选）
    └── chromium/
```

## GitHub Actions 自动构建

项目配置了 GitHub Actions 工作流，可以自动构建 Windows、macOS 和 Linux 版本。

### 🚀 快速使用

1. **从 Release 下载**：进入 [Releases](https://github.com/your-repo/releases) 页面，下载对应平台的可执行文件
2. **Windows 用户**：直接双击 `auto-login-windows-amd64.exe` 运行
3. **macOS 用户**：下载 `.app.tar.gz` 解压后双击运行，或使用可执行文件
4. **Linux 用户**：下载后添加执行权限运行

### 📦 构建方式

#### 自动构建（推送标签）

```bash
git tag v1.0.0
git push origin v1.0.0
```

会自动构建所有平台并创建 Release。

#### 手动构建（选择性）

1. 进入仓库的 **Actions** 标签页
2. 选择 **"构建和打包"** 工作流
3. 点击 **"Run workflow"**
4. 选择要构建的平台（Windows/macOS/Linux）
5. 点击运行

详细说明请查看 [GITHUB_BUILD.md](GITHUB_BUILD.md)

## 注意事项

1. **单实例运行**：程序使用锁文件机制，同一时间只能运行一个实例
2. **浏览器路径**：程序会按优先级查找浏览器：
   - 打包目录下的 `browser/chromium/`
   - Playwright 下载的浏览器
   - 系统安装的 Chrome
3. **验证码识别**：目前仅支持英文数字验证码，如需中文请修改 Tesseract 语言参数
4. **错误日志**：所有错误都会记录到 `error.log` 文件中

## 故障排除

### 浏览器启动失败

- 检查是否已安装 Playwright 浏览器：`playwright install chromium`
- 检查浏览器路径是否正确
- Windows 系统可能需要安装 Visual C++ Redistributable

### OCR 识别失败

- 检查是否已安装 Tesseract OCR
- 检查 `lang-data` 目录是否存在且包含语言数据
- 检查环境变量 `TESSDATA_PREFIX` 是否正确设置

### 无法获取锁文件

- 检查是否有其他实例正在运行
- 手动删除 `python-auto-login.lock` 文件

## 许可证

MIT License
