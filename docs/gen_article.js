// gen_article.js — 复刻 gen_article.py 逻辑（python 不可用时的替代）
// 用法: node gen_article.js <fname> <zh_title> <en_title> <meta_desc> <og_desc> <tags> <body_file>
const fs = require('fs');
const path = require('path');

const [,, fname, zh, en, meta, og, tags, bodyFile] = process.argv;
if (!fname || !bodyFile) { console.error('usage'); process.exit(1); }

const BASE = __dirname;
const tpl = fs.readFileSync(path.join(BASE, 'blog', 'ai-agent-bug-hunting.html'), 'utf8');
const body = fs.readFileSync(bodyFile, 'utf8');

const oldZh = 'AI Agent 批量修复开源项目漏洞：35 个 bug 的实战复盘';
const oldEn = 'AI-agent bug hunting at scale: a 35-bug post-mortem';
const oldMeta = '用 3 个并行审计 Agent 扫描 FastAPI 项目、从候选 bug 中筛出确定性问题、按 bounty 规则合并提交的完整方法论。附可复制的审计检查单。';
const oldOg = '并行审计 Agent + 失败测试验证 + 合并提交策略的完整复盘';
const oldTags = '#AI Agent #安全审计 #FastAPI #测试驱动';

let n = tpl;
n = n.replace(/<title>[^<]*<\/title>/, `<title>${zh}</title>`);
n = n.replace(`content="${oldZh}"`, `content="${zh}"`);
n = n.replace(`>${oldZh}</h1>`, `>${zh}</h1>`);
n = n.replace(`>${oldEn}</h1>`, `>${en}</h1>`);
n = n.replace(oldMeta, meta);
n = n.replace(oldOg, og);
n = n.replace(oldTags, tags);

// body replace: between <h2>背景</h2> and <div class="quote-block">
const start = n.indexOf('<h2>背景</h2>');
const end = n.indexOf('<div class="quote-block">');
if (start === -1 || end === -1) { console.error('markers not found'); process.exit(1); }
n = n.slice(0, start) + body + n.slice(end);

const canon = 'https://toolgen.xyz/blog/' + path.basename(fname);
n = n.replaceAll('https://toolgen.xyz/blog/ai-agent-bug-hunting.html', canon);

const now = new Date();
const ym = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
n = n.replace(/KNOWLEDGE · \d{4}-\d{2}/, `KNOWLEDGE · ${ym}`);

if (n.includes(oldZh)) console.warn('WARN: template residue remains');

const out = path.join(BASE, fname);
fs.writeFileSync(out, n, 'utf8');
console.log('OK:', fname, n.length, 'chars');