@echo off
chcp 65001 >nul
echo ============================
echo   球球跳跃 - 3D 弹球游戏
echo ============================
echo.
echo 正在启动本地服务器...
echo.
echo 浏览器将自动打开游戏页面。
echo 如未自动打开，请手动访问：
echo   http://localhost:8080
echo.
echo 按 Ctrl+C 可停止游戏
echo ============================
echo.
start http://localhost:8080
npx serve . -p 8080 --no-clipboard
