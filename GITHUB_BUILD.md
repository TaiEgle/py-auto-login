# GitHub Actions 构建指南

## 🎯 功能说明

GitHub Actions 已配置为自动构建 Windows、macOS 和 Linux 的可执行文件，支持：

- ✅ **自动构建**：推送标签时自动构建所有平台
- ✅ **手动构建**：可以选择性构建单个或多个平台
- ✅ **直接运行**：生成的文件可以直接双击运行（Windows/macOS）
- ✅ **自动发布**：构建完成后自动创建 GitHub Release

## 📦 构建方式

### 方式一：自动构建（推荐）

当推送版本标签时，会自动构建所有平台：

```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions 会自动：
1. 构建 Windows、macOS、Linux 三个平台
2. 创建 GitHub Release
3. 上传所有可执行文件

### 方式二：手动构建（选择性）

#### 1. 在 GitHub 网页上操作

1. 进入仓库的 **Actions** 标签页
2. 选择 **"构建和打包"** 工作流
3. 点击 **"Run workflow"** 按钮
4. 选择要构建的平台：
   - ✅ 构建 Windows 版本（默认开启）
   - ✅ 构建 macOS 版本（默认开启）
   - ⬜ 构建 Linux 版本（默认关闭）
5. 点击 **"Run workflow"** 开始构建

#### 2. 使用手动构建工作流

1. 进入 **Actions** 标签页
2. 选择 **"手动构建（单个平台）"** 工作流
3. 选择要构建的平台：
   - `windows` - 仅构建 Windows
   - `macos` - 仅构建 macOS
   - `linux` - 仅构建 Linux
   - `all` - 构建所有平台（需要多次运行）

## 📥 下载构建产物

### 从 Actions 页面下载

1. 进入 **Actions** 标签页
2. 点击最新的工作流运行
3. 在页面底部找到 **"Artifacts"** 部分
4. 点击对应的平台名称下载

### 从 Release 页面下载

1. 进入仓库的 **Releases** 页面
2. 找到最新版本
3. 在 **Assets** 部分下载对应平台的文件

## 🖥️ 各平台使用说明

### Windows

1. 下载 `auto-login-windows-amd64.exe`
2. **双击运行**即可
3. 首次运行会自动创建 `config.json`
4. 编辑 `config.json` 填写账号密码
5. 重新运行程序

### macOS

**方式一：使用可执行文件**

1. 下载 `auto-login-macos-amd64`
2. 在终端中运行：
   ```bash
   chmod +x auto-login-macos-amd64
   ./auto-login-macos-amd64
   ```

**方式二：使用 .app 包（推荐，可直接双击）**

1. 下载 `auto-login-macos-amd64.app.tar.gz`
2. 解压得到 `AutoLogin.app`
3. **双击运行**
4. 如果提示"无法打开"，请：
   - 右键点击应用
   - 选择"打开"
   - 或在"系统设置 > 隐私与安全性"中允许运行

### Linux

1. 下载 `auto-login-linux-amd64`
2. 添加执行权限：
   ```bash
   chmod +x auto-login-linux-amd64
   ```
3. 运行：
   ```bash
   ./auto-login-linux-amd64
   ```

## ⚠️ 注意事项

### 首次运行需要安装依赖

虽然可执行文件已经打包，但首次运行仍需要：

1. **Playwright 浏览器**：
   ```bash
   playwright install chromium
   ```

2. **Tesseract OCR**（系统级依赖）：
   - Windows: 下载安装包
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

### 配置文件位置

- 配置文件 `config.json` 与可执行文件在同一目录
- 首次运行会自动创建示例配置文件

### 文件大小

- Windows: 约 30-40 MB
- macOS: 约 30-40 MB
- Linux: 约 30-40 MB

## 🔧 构建配置说明

### 构建参数

- `--onefile`: 打包为单个可执行文件
- `--console`: 显示控制台窗口（用于调试）
- `--strip`: 去除符号信息，减小体积
- `--exclude-module`: 排除不必要的模块

### 优化措施

- 排除大型库（matplotlib, numpy, pandas 等）
- 仅包含必需的隐藏导入
- 使用 strip 减小文件体积

## 📊 构建状态

构建状态会在以下位置显示：

1. **仓库首页**：显示最新的构建状态徽章
2. **Actions 页面**：查看详细的构建日志
3. **Pull Request**：自动构建并显示状态

## 🐛 故障排除

### 构建失败

1. 查看 Actions 日志，找到失败步骤
2. 检查依赖是否正确安装
3. 确认 Python 版本兼容性（需要 3.8+）

### 可执行文件无法运行

1. **Windows**: 检查是否被杀毒软件拦截
2. **macOS**: 检查系统安全设置，允许运行
3. **Linux**: 确认已添加执行权限

### 下载文件损坏

1. 重新下载文件
2. 检查文件大小是否正常
3. 尝试从 Release 页面下载

## 📝 版本管理

### 创建新版本

```bash
# 1. 更新代码
git add .
git commit -m "更新内容"

# 2. 创建标签
git tag v1.0.1

# 3. 推送代码和标签
git push origin main
git push origin v1.0.1
```

### 版本命名规范

- 使用语义化版本：`v主版本.次版本.修订版本`
- 例如：`v1.0.0`, `v1.1.0`, `v2.0.0`

## 🔗 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyInstaller 文档](https://pyinstaller.org/)
- [项目 README](README.md)
