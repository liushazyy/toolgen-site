#!/usr/bin/env node
/* 标准知识库文章生成器（Node 版，替代 gen_article.py，因本机无 Python）。
   用法: node gen_article.mjs <文件名>.html "中文标题" "英文标题" "meta描述" "og描述" "#标签" <正文文件> [引文]
   自动处理: title/og:title/h1(中英)/meta desc/og desc/tags/quote-block/og:url/canonical 全部替换，杜绝模板残留。 */
const fs = require('fs');
const path = require('path');

const BASE = __dirname + '/../docs';
const TPL = path.join(BASE, 'blog', 'ai-agent-bug-hunting.html');

function main() {
  const args = process.argv.slice(2);
  if (args.length < 7) {
    console.log('用法: node gen_article.mjs <fname> <zh_title> <en_title> <meta_desc> <og_desc> <tags> <body_file> [quote]');
    return 1;
  }
  const [fname, zh, en, meta, og, tags, bodyFile, quote] = args;
  const tpl = fs.readFileSync(TPL, 'utf8');
  const body = fs.readFileSync(bodyFile, 'utf8');

  const oldZh = 'AI Agent 批量修复开源项目漏洞：35 个 bug 的实战复盘';
  const oldEn = 'AI-agent bug hunting at scale: a 35-bug post-mortem';
  const oldMeta = '用 3 个并行审计 Agent 扫描 FastAPI 项目、从候选 bug 中筛出确定性问题、按 bounty 规则合并提交的完整方法论。附可复制的审计检查单。';
  const oldOg = '并行审计 Agent + 失败测试验证 + 合并提交策略的完整复盘';
  const oldTags = '#AI Agent #安全审计 #FastAPI #测试驱动';

  let out = tpl
    .replace(/<title>[^<]*<\/title>/, `<title>${zh}</title>`)
    .replace(new RegExp(`content="${oldZh}"`), `content="${zh}"`)
    .replace(new RegExp(`>${oldZh}</h1>`), `>${zh}</h1>`)
    .replace(new RegExp(`>${oldEn}</h1>`), `>${en}</h1>`)
    .replace(oldMeta, meta)
    .replace(oldOg, og)
    .replace(oldTags, tags);
  // og:url + canonical 自动校准到本文件（fname 含 blog/ 前缀，URL 用完整相对路径拼接）
  const absUrl = `https://toolgen.xyz/${fname}`;
  out = out.replace(/content="https:\/\/toolgen\.xyz\/blog\/[^"]*"/, `content="${absUrl}"`);
  out = out.replace(/href="https:\/\/toolgen\.xyz\/blog\/[^"]*"/, `href="${absUrl}"`);

  const start = out.indexOf('<h2>背景</h2>');
  const endMarker = '<div class="quote-block">';
  const end = out.indexOf(endMarker);
  if (start === -1 || end === -1) { console.log('模板标记未找到'); return 1; }
  out = out.slice(0, start) + body + out.slice(end);

  // 替换引文（若有）
  if (quote) {
    const qStart = out.indexOf(endMarker);
    const qEnd = out.indexOf('</div>', qStart);
    if (qStart !== -1 && qEnd !== -1) {
      out = out.slice(0, qStart + endMarker.length) + '\n        ' + quote + '\n      ' + out.slice(qEnd);
    }
  }

  // 校验
  if (out.includes(oldZh)) { console.log('警告: 仍有模板残留'); }
  const outPath = path.join(BASE, fname);
  fs.writeFileSync(outPath, out, 'utf8');
  console.log('OK:', fname, out.length, 'chars');
  return 0;
}

process.exit(main());