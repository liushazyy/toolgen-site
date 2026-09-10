# -*- coding: utf-8 -*-
"""给 toolgen-site 全站 HTML 装 busuanzi 访客统计。
幂等：已装过的跳过。页脚 f-bottom 加 UV/PV 显示，</body> 前加脚本。
"""
import io, os, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"C:\Users\admin\toolgen-site\docs"

SCRIPT_TAG = '<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>\n'
FOOTER_SPAN = ('      <span id="busuanzi_container_site_uv" style="display:none">'
               '<span data-lang="zh">访客</span><span data-lang="en">Visitors</span> '
               '<span id="busuanzi_value_site_uv"></span></span>\n'
               '      <span id="busuanzi_container_site_pv" style="display:none">'
               '<span data-lang="zh">浏览</span><span data-lang="en">Views</span> '
               '<span id="busuanzi_value_site_pv"></span></span>\n')

files = sorted(glob.glob(os.path.join(BASE, "*.html"))) + sorted(glob.glob(os.path.join(BASE, "blog", "*.html")))
added_script = added_footer = skipped = 0

for fp in files:
    with open(fp, encoding="utf-8") as f:
        html = f.read()
    if "busuanzi" in html:
        skipped += 1
        continue
    changed = False
    # 1. 页脚显示（找 f-bottom 内的 © 版权行后插入）
    marker = '<span>© 2026 玄境科技 Xuanjing Tech · toolgen.xyz</span>'
    if marker in html:
        html = html.replace(marker, marker + "\n" + FOOTER_SPAN.rstrip("\n"), 1)
        added_footer += 1
        changed = True
    # 2. 统计脚本（</body> 前）
    if "</body>" in html:
        html = html.replace("</body>", SCRIPT_TAG + "</body>", 1)
        added_script += 1
        changed = True
    if changed:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(html)

print(f"共 {len(files)} 个文件：装脚本 {added_script}，加页脚计数 {added_footer}，已装过跳过 {skipped}")
