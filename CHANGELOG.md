# 更新日志

本项目所有重要变更均记录于此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [1.0.0] - 2026-07-04

首个正式版本：基于 Three.js 的 3D 球球跳跃游戏，含完整关卡玩法、移动端适配与自动部署。

### 新增

- 3D 球球跳跃核心玩法：多类型彩色跳板、节拍同步弹跳、黑洞过关、5 关卡进度
- 渐进加速系统：速度随距离递增，Type 4 加速块叠加并随时间衰减
- 循环播放的背景音乐（bgm.mp3）
- 开局提示，第一关加入加速机制
- 广告播放期间暂停背景音乐，复活后自动恢复
- 手机触摸支持：`touchstart` / `touchmove` 控制球体移动
- 使用 localStorage 保存关卡进度
- GitHub Pages 自动部署（gh-pages 分支）
- 游戏遥测系统：客户端事件埋点、逐帧性能记录、WebGL 上下文丢失/恢复与错误上报，配套 Python 接收服务器（`server.py`）；默认仅在本地开发环境启用

### 变更

- 移动端性能优化，适配 Android / iOS（粒子数、几何精度、阴影、像素比按 `isMobile` 分级）
- 部署方案改用 gh-pages 分支，更加可靠

### 修复

- BOOST 指示器不再被渐进速度误触发，仅 Type 4 加速块激活
- 微信浏览器兼容性：缓存控制、ES2015 构建目标、WebGL 回退
- `isMobile` 声明移到 `starCount` 之前，避免 ReferenceError 导致模块崩溃
- 跨设备兼容：采用 IIFE 格式 + JS 内联，手机/电脑均可直接打开即玩
- 手机端渲染问题：关卡卡片改为静态 HTML，脚本移至 body 末尾

[Unreleased]: https://github.com/zhihanzhe/ball-game/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/zhihanzhe/ball-game/releases/tag/v1.0.0
