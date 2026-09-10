# -*- coding: utf-8 -*-
"""修复 blog/github-actions-content-pipeline.html：补 quote-block + 闭合 + 页脚 + 脚本 + busuanzi。
页脚与脚本结构取自同目录正常文章 liuyao-najia.html，保证全站一致。
"""
import io, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"C:\Users\admin\toolgen-site\docs\blog"
BROKEN = BASE + r"\github-actions-content-pipeline.html"
REF = BASE + r"\liuyao-najia.html"

with open(BROKEN, encoding="utf-8") as f:
    html = f.read()
with open(REF, encoding="utf-8") as f:
    ref = f.read()

if "</html>" in html:
    print("已含闭合标签，无需修复")
    sys.exit(0)

# 从参考文章提取：footer 起 到 </html> 结束（含脚本与 busuanzi）
i = ref.find("<footer")
j = ref.find("</html>") + len("</html>")
assert i != -1 and j > i, "参考文章结构异常"
tail = ref[i:j]

# 参考文章的 footer 内链接用相对路径 ../，与本文同目录，无需改写
QUOTE = '''      <div class="quote-block">
        自动化流水线的价值不在省那几分钟，而在让搜索引擎与访客都看到「这个站是活的」。
        每周稳定产出，是收录与排名最朴素的前提。
      </div>

    </div>
  </div>
</section>

'''

html = html.rstrip("\r\n ") + "\n\n" + QUOTE + tail + "\n"

with open(BROKEN, "w", encoding="utf-8") as f:
    f.write(html)

# 校验
for need in ("</html>", "</body>", "<footer", "busuanzi", "quote-block"):
    print(("OK  " if need in html else "MISS"), need)
print("行数:", html.count("\n"))
print("模板残留检查 '35 个 bug':", html.count("35 个 bug"))
