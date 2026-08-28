# -*- coding: utf-8 -*-
"""Fix template-residue quote blocks across blog articles."""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "blog")

QUOTES = {
    "github-pages-custom-domain.html": "自定义域名就两件事：DNS 的 CNAME 指对地方、Pages 设置里填对域名，剩下的交给 Let's Encrypt 自动续期。",
    "solana-data-automation.html": "链上数据不会说谎，但解析规则会：先定好账户模型与 RPC 限流策略，自动化才不会在凌晨三点断掉。",
    "local-llm-deployment.html": "本地模型的自由，是用显存和耐心换来的：量化等级决定速度，上下文长度决定它能帮你多久。",
    "mcp-protocol-intro.html": "MCP 的野心是把工具调用标准化：模型不用为每个平台学一套新协议，一次接入，处处可用。",
    "multi-agent-collaboration.html": "多 Agent 协作的瓶颈从来不是单个模型的能力，而是任务拆解与上下文交接的清晰度。",
    "one-person-company.html": "一人公司的护城河不是省钱，而是用自动化把重复劳动压到最低，把时间留给真正需要判断力的事。",
    "prompt-engineering-task-brief.html": "提示词工程的第一性原理：把任务书写到「换个执行者也能交付同一结果」，模型才能稳定复现你的意图。",
    "smart-contract-audit-methodology.html": "审计不是找茬，是给资金上保险：先跑通威胁模型再谈漏洞清单，风险排序比漏洞数量更重要。",
    "dolphin-mcp-pilot-nl-workflow.html": "自然语言工作流的价值，是把「会做」变成「能重复做」：一次说清流程，Agent 就能替你跑一百遍。",
    "github-actions-content-pipeline.html": "内容管线的意义在于发布不再是动作，而是状态：push 即部署，人人可复现。",
}

for fname, quote in QUOTES.items():
    path = os.path.join(BASE, fname)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    new_html, n = re.subn(
        r'(<div class="quote-block">\s*)(.*?)(\s*</div>)',
        lambda m: m.group(1) + "        " + quote + m.group(3),
        html, count=1, flags=re.S,
    )
    if n != 1:
        print("SKIP (no quote-block):", fname); continue
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_html)
    print("FIXED:", fname)
