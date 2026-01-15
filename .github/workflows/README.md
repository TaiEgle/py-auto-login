# GitHub Actions 工作流说明

## 工作流列表

### 1. 构建和打包 (build.yml)

**触发条件：**
- 推送版本标签（`v*`）：自动构建所有平台
- 手动触发（workflow_dispatch）：可选择构建平台
- Pull Request：自动构建所有平台（用于测试）

**功能：**
- 构建 Windows、macOS、Linux 可执行文件
- 为 macOS 创建 .app 包（可直接双击）
- 自动创建 GitHub Release
- 上传构建产物

**手动触发选项：**
- `build_windows`: 是否构建 Windows 版本（默认：true）
- `build_macos`: 是否构建 macOS 版本（默认：true）
- `build_linux`: 是否构建 Linux 版本（默认：false）

### 2. 手动构建（单个平台）(manual-build.yml)

**触发条件：**
- 仅手动触发（workflow_dispatch）

**功能：**
- 快速构建单个平台
- 适合快速测试或单独发布某个平台

**选项：**
- `platform`: 选择构建平台（windows/macos/linux/all）

## 使用示例

### 自动构建（推送标签）

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 手动构建（选择平台）

1. 进入 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择 **"构建和打包"**
4. 点击 **"Run workflow"**
5. 选择要构建的平台
6. 点击运行

## 构建产物

### Windows
- `auto-login-windows-amd64.exe` - 可直接双击运行

### macOS
- `auto-login-macos-amd64` - 可执行文件
- `auto-login-macos-amd64.app.tar.gz` - .app 包（推荐，可直接双击）

### Linux
- `auto-login-linux-amd64` - 可执行文件（需添加执行权限）

## 下载位置

1. **Actions 页面**：每个构建运行的 Artifacts 部分
2. **Releases 页面**：版本发布后的 Assets 部分
