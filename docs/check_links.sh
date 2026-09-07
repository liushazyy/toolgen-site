#!/bin/bash
# 纯 bash 路径映射死链检查（兼容 MSYS/git-bash）
cd /c/Users/admin/toolgen-site/docs || exit 1
check_file() {
  local f="$1" dir link target
  dir=$(dirname "$f")
  while IFS= read -r link; do
    case "$link" in
      http*|mailto:*|tel:*|"#"*|"") continue ;;
    esac
    link=${link%%#*}
    [ -z "$link" ] && continue
    if [ "$dir" = "." ]; then
      # 根目录页面：链接要么是根相对，要么是 blog/xxx
      case "$link" in
        blog/*) target="$link" ;;
        *) target="$link" ;;
      esac
    else
      # blog 目录页面：../ 回到根，裸链接是同目录
      case "$link" in
        ../*) target="${link#../}" ;;
        *) target="$dir/$link" ;;
      esac
    fi
    if [ ! -f "$target" ]; then
      echo "DEAD: $f -> $link (resolved: $target)"
    fi
  done < <(grep -hoE 'href="[^"]*"' "$f" | sed 's/href="//; s/"$//')
}
for f in index.html products.html services.html work.html tools.html blog.html about.html contact.html 404.html; do
  check_file "$f"
done
for f in blog/*.html; do
  check_file "$f"
done
echo "deadlink-check-done"