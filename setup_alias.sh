#!/bin/bash
# 创建 Python 别名脚本

echo "正在为 zsh 配置 Python 别名..."

# 检查 shell 类型
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    SHELL_CONFIG="$HOME/.zshrc"
fi

# 检查是否已存在别名
if grep -q "alias python=python3" "$SHELL_CONFIG" 2>/dev/null; then
    echo "⚠️  别名已存在，跳过..."
else
    echo "" >> "$SHELL_CONFIG"
    echo "# Python 别名" >> "$SHELL_CONFIG"
    echo "alias python=python3" >> "$SHELL_CONFIG"
    echo "alias pip=pip3" >> "$SHELL_CONFIG"
    echo "✅ 别名已添加到 $SHELL_CONFIG"
    echo ""
    echo "请运行以下命令使别名生效："
    echo "  source $SHELL_CONFIG"
    echo ""
    echo "或者重新打开终端"
fi
