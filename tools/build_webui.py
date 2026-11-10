"""Rebuild the editable dashboard into MaiBot's self-contained custom document."""
from pathlib import Path
import base64
import re

root = Path(__file__).resolve().parents[1]
dashboard = root / 'pages/dashboard'
html = (dashboard / 'index.html').read_text(encoding='utf-8')
html = html.replace('<script src="./assets/js/i18n.js">', '<script src="./assets/js/maibot_bridge.js"></script>\n  <script src="./assets/js/i18n.js">')
html = re.sub(r'<link rel="stylesheet" href="\./([^"]+)">', lambda m: '<style>' + (dashboard / m[1]).read_text(encoding='utf-8') + '</style>', html)
html = re.sub(r'<script src="\./([^"]+)"></script>', lambda m: '<script>\n' + (dashboard / m[1]).read_text(encoding='utf-8').replace('</script', '<\\/script') + '\n</script>', html)
html = html.replace('./assets/images/logo.png', 'data:image/png;base64,' + base64.b64encode((root / 'logo.png').read_bytes()).decode())
html = html.replace('API Aggregator', 'API 聚合')
(root / 'webui').mkdir(exist_ok=True)
(root / 'webui/index.html').write_text(html, encoding='utf-8')
print('Built webui/index.html:', len(html.encode('utf-8')), 'bytes')
