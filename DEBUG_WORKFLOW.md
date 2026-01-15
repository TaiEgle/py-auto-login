# GitHub Actions 调试指南

## 🔍 如何查看失败原因

### 方法 1: 查看 Actions 日志

1. 进入 GitHub 仓库
2. 点击 **Actions** 标签
3. 找到失败的工作流运行（红色 ❌）
4. 点击进入查看详情
5. 点击失败的 job（例如 "build"）
6. 展开每个步骤查看详细日志

### 方法 2: 查看具体错误

在日志中查找：
- `Error:` - 错误信息
- `Failed` - 失败步骤
- `exit code 1` - 命令失败
- `No such file` - 文件不存在

## 🛠️ 已修复的问题

### 1. 条件判断优化

修复了 `if` 条件，现在：
- 手动触发时正确处理默认值（空字符串视为 true）
- 推送标签时构建所有平台
- Pull Request 时构建所有平台

### 2. 添加调试步骤

每个 job 开始时会输出：
- 事件类型
- 平台选择
- 矩阵配置

### 3. 添加构建产物检查

在复制文件前检查：
- dist 目录是否存在
- 可执行文件是否生成
- 文件大小是否正常

### 4. 错误处理

- 添加 `continue-on-error: false` 确保错误不被忽略
- 添加文件存在性检查
- 添加详细的错误信息

## 📋 测试步骤

### 测试 1: 手动触发单个平台

1. 进入 Actions 页面
2. 选择 "构建和打包" 工作流
3. 点击 "Run workflow"
4. 选择平台（例如：Windows）
5. 取消其他平台
6. 运行并查看日志

### 测试 2: 查看调试信息

在日志中找到 "调试信息" 步骤，确认：
- Event 正确
- Platform 正确
- Matrix 配置正确

### 测试 3: 检查构建过程

查看 "构建可执行文件" 步骤：
- PyInstaller 是否成功执行
- 是否有错误或警告
- 构建是否完成

## 🔧 如果仍然失败

### 方案 1: 使用简化版工作流

已创建 `build-simple.yml`，使用更简单的逻辑：

1. 重命名文件：
   ```bash
   mv .github/workflows/build.yml .github/workflows/build.yml.bak
   mv .github/workflows/build-simple.yml .github/workflows/build.yml
   ```

2. 提交并推送：
   ```bash
   git add .github/workflows/
   git commit -m "使用简化版工作流"
   git push
   ```

### 方案 2: 检查具体错误

根据错误信息：

**如果显示 "Job was skipped"**：
- 检查条件判断
- 确认手动触发时选择了正确的平台

**如果显示 "Command failed"**：
- 查看命令的完整输出
- 检查依赖是否正确安装

**如果显示 "File not found"**：
- 确认文件已提交到仓库
- 检查文件路径是否正确

### 方案 3: 本地测试

在本地测试构建过程：

```bash
# 安装依赖
pip3 install -r requirements.txt
pip3 install pyinstaller

# 测试构建
python3 build.py
```

## 📝 常见问题

### Q: 为什么没有错误信息？

**A:** 可能的原因：
1. Job 被跳过（显示为灰色，不是失败）
2. 错误被静默忽略
3. 需要展开步骤查看详细日志

### Q: 如何查看被跳过的 Job？

**A:** 
1. 点击被跳过的 job
2. 查看 "Why was this job skipped?" 部分
3. 检查条件判断逻辑

### Q: 构建成功但找不到文件？

**A:**
1. 检查 "检查构建产物" 步骤
2. 确认 dist 目录存在
3. 查看文件路径是否正确

## 🆘 需要帮助？

如果问题仍然存在，请提供：

1. **工作流运行链接**
2. **失败步骤的完整日志**
3. **调试信息步骤的输出**
4. **具体错误信息**

这样我可以更准确地帮你解决问题。
