#!/usr/bin/env python3
"""遥测数据接收器 —— 启动后在控制台实时打印游戏上报的所有事件"""
import json, sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

PORT = 8080

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('content-length', 0))
            body = self.rfile.read(length).decode('utf-8')
            data = json.loads(body)

            device = data.get('device', {})
            events = data.get('events', [])
            reason = data.get('session_end_reason', '?')
            sid = device.get('session_id', 'unknown')[:8]

            print(f"\n{'─'*60}")
            print(f"📡 [{datetime.now().strftime('%H:%M:%S')}] 收到 {len(events)} 条事件 (session={sid}... end={reason})")
            for ev in events:
                name = ev.get('event', '?')
                lvl = ev.get('level', '?')
                dist = ev.get('distance', 0)

                details = ''
                if name == 'death':
                    details = f" 原因={ev.get('death_type')}  combo={ev.get('combo')}  dist={dist:.1f}m"
                elif name == 'level_start':
                    details = f" 关卡={lvl} 名称={ev.get('level_name')}"
                elif name == 'level_complete':
                    details = f" 关卡={lvl}  combo={ev.get('combo')}  dist={dist:.1f}m"
                elif name == 'frame_stats':
                    details = f" fps={ev.get('fps')}  p95={ev.get('p95_dt_ms')}ms  jank={ev.get('jank_frames')}/{ev.get('sample_count')}"
                elif name == 'audio_init':
                    details = f" 状态={ev.get('status')} 节拍={ev.get('beat_count')}"
                elif name == 'global_error':
                    details = f" 类型={ev.get('type')} msg={str(ev.get('message',''))[:60]}"
                elif name == 'webgl_context_lost':
                    details = f" level={lvl} dist={dist:.1f}m"
                elif name == 'webgl_context_restored':
                    details = f" 已恢复"
                elif name == 'webgl_init_failed':
                    details = f" error={ev.get('error','')[:60]}"
                elif name == 'ad_watch_start':
                    details = f" level={lvl}"
                elif name == 'ad_completed':
                    details = f" level={lvl}"
                elif name == 'resume_used':
                    details = f" dist={dist:.1f}m combo={ev.get('combo')}"
                elif name == 'all_levels_complete':
                    details = f" 全部{ev.get('total_levels')}关通关!"
                elif name == 'objective_spawned':
                    details = f" 需连续{ev.get('combo_required')}跳"

                print(f"  [{name:22s}] {details}")
            sys.stdout.flush()

        except Exception as e:
            print(f"  ⚠️ 解析失败: {e}")

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        pass  # 静默 HTTP 日志

print(f"""
╔══════════════════════════════════════╗
║     🎯 遥测数据接收器                ║
║                                     ║
║  监听端口: {PORT}                      ║
║  端点地址: http://localhost:{PORT}/telemetry ║
║                                     ║
║  请确认 index.html 中 ENDPOINT 为:  ║
║  http://localhost:{PORT}/telemetry     ║
║                                     ║
║  启动游戏后，这里会实时打印所有事件  ║
║  按 Ctrl+C 停止                      ║
╚══════════════════════════════════════╝
""")

HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
