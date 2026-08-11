#!/usr/bin/env bash
# gen_article.sh - bash/sed 版文章生成器（等价于 gen_article.py 逻辑，适配无 python/perl 环境）
# 用法: gen_article.sh <fname> <zh_title> <en_title> <meta_desc> <og_desc> <tags> <body_file>
set -euo pipefail
cd "$(dirname "$0")"
FNAME="$1"; ZH="$2"; EN="$3"; META="$4"; OG="$5"; TAGS="$6"; BODY="$7"
TPL="blog/ai-agent-bug-hunting.html"
OUT="blog/$FNAME"
OLD_ZH="AI Agent 批量修复开源项目漏洞：35 个 bug 的实战复盘"
OLD_EN="AI-agent bug hunting at scale: a 35-bug post-mortem"
OLD_META="用 3 个并行审计 Agent 扫描 FastAPI 项目、从候选 bug 中筛出确定性问题、按 bounty 规则合并提交的完整方法论。附可复制的审计检查单。"
OLD_OG="并行审计 Agent + 失败测试验证 + 合并提交策略的完整复盘"
OLD_TAGS="#AI Agent #安全审计 #FastAPI #测试驱动"
OLD_CANON="https://toolgen.xyz/blog/ai-agent-bug-hunting.html"
NEW_CANON="https://toolgen.xyz/blog/$FNAME"

# sed 转义：& 和分隔符 /
esc() { printf '%s' "$1" | sed 's/[\/&]/\\&/g'; }
E_ZH=$(esc "$ZH"); E_EN=$(esc "$EN"); E_META=$(esc "$META"); E_OG=$(esc "$OG"); E_TAGS=$(esc "$TAGS")
E_OLD_CANON=$(esc "$OLD_CANON"); E_NEW_CANON=$(esc "$NEW_CANON")

sed -e "s|<title>[^<]*</title>|<title>$E_ZH</title>|" \
    -e "s|content=\"$OLD_ZH\"|content=\"$E_ZH\"|" \
    -e "s|>$OLD_ZH</h1>|>$E_ZH</h1>|" \
    -e "s|>$OLD_EN</h1>|>$E_EN</h1>|" \
    -e "s|$OLD_META|$E_META|" \
    -e "s|$OLD_OG|$E_OG|" \
    -e "s|$OLD_TAGS|$E_TAGS|" \
    -e "s|$E_OLD_CANON|$E_NEW_CANON|g" \
    "$TPL" > "$OUT.tmp"

# 正文替换：取模板头部(到<h2>背景</h2>为止) + 新正文 + 模板尾部(从<div class="quote-block">起)
head_part=$(sed -n '1,/<h2>背景<\/h2>/p' "$OUT.tmp" | sed '$d')   # 含 <h2>背景</h2> 之前所有行
tail_part=$(sed -n '/<div class="quote-block">/,$p' "$OUT.tmp")
{ printf '%s\n' "$head_part"; cat "$BODY"; printf '%s\n' "$tail_part"; } > "$OUT"
rm -f "$OUT.tmp"

# 校验
if grep -q "35 个 bug" "$OUT"; then echo "ERROR: 模板残留"; exit 1; fi
if ! grep -q "<title>$ZH</title>" "$OUT"; then echo "ERROR: title 未替换"; exit 1; fi
if ! grep -q "og:title\" content=\"$ZH\"" "$OUT"; then echo "ERROR: og:title 未替换"; exit 1; fi
if ! grep -q ">$ZH</h1>" "$OUT"; then echo "ERROR: h1 未替换"; exit 1; fi
if ! grep -q "canonical\" href=\"$NEW_CANON\"" "$OUT"; then echo "ERROR: canonical 未替换"; exit 1; fi
if ! grep -q "og:url\" content=\"$NEW_CANON\"" "$OUT"; then echo "ERROR: og:url 未替换"; exit 1; fi
echo "OK: $OUT ($(wc -c < "$OUT") bytes)"
