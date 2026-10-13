#!/bin/bash
# MathTeacherPage - GitHub Token 安全配置脚本
# 功能：引导用户生成 token 并安全存储到 macOS Keychain

set -e

echo "=========================================="
echo "  MathTeacherPage - Token 安全配置"
echo "=========================================="
echo ""

# 检查是否已配置 remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE_URL" ]; then
  echo "✗ 未配置 git remote"
  echo "正在添加..."
  git remote add origin https://github.com/tsing-cv/MathTeacherPage.git
  echo "✓ remote 已添加"
fi

# 确保 remote URL 不含 token
if [[ "$REMOTE_URL" == *@github.com* ]]; then
  echo "⚠ remote URL 包含 token，正在清理..."
  git remote set-url origin https://github.com/tsing-cv/MathTeacherPage.git
  echo "✓ remote URL 已清理"
fi

echo ""
echo "步骤 1：生成 GitHub Personal Access Token"
echo "----------------------------------------"
echo ""
echo "请在浏览器中打开以下链接："
echo "  https://github.com/settings/tokens/new"
echo ""
echo "配置："
echo "  • Note: MathTeacherPage"
echo "  • Expiration: 90 days (或 No expiration)"
echo "  • 勾选: repo (完整仓库权限)"
echo ""
echo "点击 Generate token 后，复制 token（ghp_ 开头）"
echo ""

# 读取 token
read -p "请粘贴新 Token: " TOKEN

if [ -z "$TOKEN" ]; then
  echo "✗ Token 不能为空"
  exit 1
fi

if [[ ! "$TOKEN" =~ ^ghp_ ]]; then
  echo "⚠ Token 格式可能不正确（应以 ghp_ 开头）"
  read -p "继续？(y/n): " CONTINUE
  if [ "$CONTINUE" != "y" ]; then
    exit 1
  fi
fi

echo ""
echo "步骤 2：存储 Token 到 macOS Keychain"
echo "----------------------------------------"

# 存储到 Keychain
printf "protocol=https\nhost=github.com\nusername=tsing-cv\npassword=$TOKEN\n" | git credential-osxkeychain store

echo "✓ Token 已安全存储到 Keychain"

echo ""
echo "步骤 3：测试推送"
echo "----------------------------------------"

cd "$(dirname "$0")"
git push origin main 2>&1

if [ $? -eq 0 ]; then
  echo ""
  echo "✓ 推送成功！"
else
  echo ""
  echo "✗ 推送失败，请检查 Token 是否正确"
  exit 1
fi

echo ""
echo "=========================================="
echo "  ✓ Token 配置完成！"
echo "=========================================="
echo ""
echo "安全提示："
echo "  • Token 存储在 macOS Keychain（加密）"
echo "  • deploy.sh 会自动使用 Keychain 中的 Token"
echo "  • 不要将 Token 分享给他人"
echo "  • 定期在 https://github.com/settings/tokens 轮换 Token"
echo ""
echo "部署命令："
echo "  ./deploy.sh"
echo ""
