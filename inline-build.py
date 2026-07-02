"""构建后处理：将 JS 内嵌到 HTML 中，去除 type=module，生成单文件"""
import re, sys, os, glob

dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
html_path = os.path.join(dist_dir, 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 找到 script 标签引用的 JS 文件
match = re.search(r'<script\s+type="module"\s+crossorigin\s+src="(\./assets/[^"]+\.js)"', html)
if not match:
    print('ERROR: 未找到 JS 引用')
    sys.exit(1)

js_rel = match.group(1)
js_path = os.path.join(dist_dir, js_rel)

if not os.path.exists(js_path):
    print(f'ERROR: JS 文件不存在: {js_path}')
    sys.exit(1)

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# 替换：内联 JS，去除 type=module
old_tag = match.group(0)
new_tag = f'<script>{js_content}</script>'
html = html.replace(old_tag, new_tag)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# 删除 assets 目录（已内联）
import shutil
assets_dir = os.path.join(dist_dir, 'assets')
if os.path.exists(assets_dir):
    shutil.rmtree(assets_dir)

size_kb = os.path.getsize(html_path) / 1024
print(f'OK: 内联完成 → {html_path} ({size_kb:.0f} KB)')
