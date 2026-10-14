#!/usr/bin/env bash
# Inlines the subset display font into index.html (keeps the page dependency-free),
# then regenerates the info pages, sitemap.xml and robots.txt (tools/pages.py).
set -e; cd "$(dirname "$0")"
python3 - <<'PY'
import base64
f=base64.b64encode(open('fonts/lilita-subset.woff','rb').read()).decode()
open('index.html','w').write(open('index.template.html').read().replace('__FONT__',f))
PY
echo "index.html built"
python3 tools/pages.py
# Copy protection: domain lock + obfuscation of the inline game-hub script (skips if ZG_NOPROTECT=1)
[ "${ZG_NOPROTECT:-}" = 1 ] || python3 /workspace/zaib-common/protect.py index.html
