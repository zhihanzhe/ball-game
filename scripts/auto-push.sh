#!/usr/bin/env bash
# auto-push.sh — 自动推送 origin/main..HEAD 中未推送的提交
# 失败时每 10s 重试，直到推送成功。只推 origin main，绝不 --force。
# 由 post-commit 钩子分离调用，也可手动执行：bash scripts/auto-push.sh

set -u
cd "$(git rev-parse --show-toplevel)" || exit 1

LOCK_DIR=".git/auto-push.lock"

# 简单锁：防止多个钩子并发重复推送
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    echo "auto-push: 已有推送进程在运行，退出"
    exit 0
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null' EXIT

# 没有待推送提交则直接退出
if [ "$(git rev-list origin/main..HEAD --count 2>/dev/null || echo 0)" = "0" ]; then
    echo "auto-push: 没有待推送的提交"
    exit 0
fi

echo "auto-push: 开始推送 $(git rev-list origin/main..HEAD --count) 个提交..."
attempt=0
until git push origin main 2>&1; do
    attempt=$((attempt + 1))
    echo "auto-push: $(date '+%H:%M:%S') 第 ${attempt} 次推送失败，10s 后重试..."
    sleep 10
done

echo "auto-push: $(date '+%H:%M:%S') 推送成功"
