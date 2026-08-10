# -*- coding: utf-8 -*-
"""标准知识库文章生成器（供每日优化任务复用）。
用法：python gen_article.py <文件名>.html "中文标题" "英文标题" "meta描述" "og描述" "标签" 正文文件路径
自动处理：title/og:title/h1(中英)/meta desc/og desc/tags 全部替换，杜绝模板残留。
"""
import io, sys, os, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(BASE, "ai-agent-bug-hunting.html")  # 干净的模板源

def main():
    if len(sys.argv) < 8:
        print("用法: gen_article.py <fname> <zh_title> <en_title> <meta_desc> <og_desc> <tags> <body_file>")
        return 1
    fname, zh_title, en_title, meta_desc, og_desc, tags, body_file = sys.argv[1:8]
    with open(TPL, encoding="utf-8") as f:
        tpl = f.read()
    with open(body_file, encoding="utf-8") as f:
        body = f.read()
    old_zh = "AI Agent 批量修复开源项目漏洞：35 个 bug 的实战复盘"
    old_en = "AI-agent bug hunting at scale: a 35-bug post-mortem"
    old_meta = "用 3 个并行审计 Agent 扫描 FastAPI 项目、从候选 bug 中筛出确定性问题、按 bounty 规则合并提交的完整方法论。附可复制的审计检查单。"
    old_og = "并行审计 Agent + 失败测试验证 + 合并提交策略的完整复盘"
    old_tags = "#AI Agent #安全审计 #FastAPI #测试驱动"

    new = tpl
    # title 带后缀 " | 玄境科技知识库"，用正则替换开头部分
    new = re.sub(r"<title>[^<]*</title>", "<title>" + zh_title + "</title>", new, count=1)
    new = new.replace('content="' + old_zh + '"', 'content="' + zh_title + '"')  # og:title
    new = new.replace('>' + old_zh + '</h1>', '>' + zh_title + '</h1>')  # h1 zh
    new = new.replace('>' + old_en + '</h1>', '>' + en_title + '</h1>')  # h1 en
    new = new.replace(old_meta, meta_desc)
    new = new.replace(old_og, og_desc)
    new = new.replace(old_tags, tags)
    # 替换正文
    start = new.find("<h2>背景</h2>")
    end_marker = '<div class="quote-block">'
    end = new.find(end_marker)
    if start == -1 or end == -1:
        print("模板标记未找到")
        return 1
    new = new[:start] + body + new[end:]
    # 校验无残留
    if old_zh in new and "og:title" in new:
        print("警告: 仍有模板残留")
    path = os.path.join(BASE, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    print("OK:", fname, len(new), "chars")

if __name__ == "__main__":
    sys.exit(main())
