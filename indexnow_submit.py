# -*- coding: utf-8 -*-
"""Submit all sitemap URLs to Bing IndexNow via proxy."""
import io, json, sys, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

urls = [l.strip() for l in open("docs/sitemap.txt", encoding="utf-8") if l.strip()]
payload = {
    "host": "toolgen.xyz",
    "key": "xuanjing2026toolgen",
    "keyLocation": "https://toolgen.xyz/ix-key.txt",
    "urlList": urls,
}
req = urllib.request.Request(
    "https://www.bing.com/indexnow",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST",
)
proxy = urllib.request.ProxyHandler({"https": "http://127.0.0.1:7890", "http": "http://127.0.0.1:7890"})
opener = urllib.request.build_opener(proxy)
try:
    resp = opener.open(req, timeout=30)
    print("HTTP", resp.status, "|", resp.read().decode("utf-8", "replace")[:300])
except urllib.error.HTTPError as e:
    print("HTTP", e.code, "|", e.read().decode("utf-8", "replace")[:300])
print("submitted", len(urls), "urls")
