# 更新日志

本项目所有重要变更均记录于此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [1.1.1] - 2026-07-23

### 修复

- 移动端点击右下角静音按钮时，触摸事件不再被当作游戏控制输入，修复误触导致小球瞬间飞出界外死亡的问题

## [1.1.0] - 2026-07-23

### 新增

- 键盘控制：←/→ 或 A/D 持续移动小球，与鼠标/触摸并存
- 暂停功能：Esc / P 切换，暂停时显示「已暂停」遮罩并暂停背景音乐，恢复时重置帧计时避免突跳
- 静音功能：M 键或右下角按钮切换，节拍音效经 masterGain 总线统一静音，状态持久化到 localStorage
- 边缘容错：超出轨道边缘有 0.3 秒宽限，期间线框球闪红警告，回到安全区即恢复
- 色弱友好：类型2/3 方块箭头下方叠加颜色对应符号（粉=圆、黄=三角、蓝=方）
- 页面标题改为「球球跳跃 - 3D 弹球游戏」，开局提示补充操作说明

### 变更

- 帧率无关化：主循环统一使用真实帧间隔 dt（及 60fps 等效系数 dt60），替换全部硬编码 0.016 帧步长，高刷屏与低端机速度一致
- 弹跳改为相位累加器（bouncePhase），节拍间距切换时高度不再跳变
- 关卡数值重调：第 1 关基础速度 2.0 → 1.0；通关跳跃次数第 3 关 20 → 25、第 4 关 200 → 60、第 5 关 2000 → 120
- 移除未使用的 OrbitControls（相机本来就固定）

### 修复

- 木板几何体/材质改为共享资源，回收与清场时不再新建也不 dispose，修复长局运行的 GPU 资源泄漏

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

[Unreleased]: https://github.com/zhihanzhe/ball-game/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/zhihanzhe/ball-game/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/zhihanzhe/ball-game/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/zhihanzhe/ball-game/releases/tag/v1.0.0
