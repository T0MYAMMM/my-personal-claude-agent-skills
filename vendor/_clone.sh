#!/usr/bin/env bash
# Clone every repo listed in _repos.txt into vendor/<owner>__<repo>/.
# Strips .git on success. Skips already-cloned. Records failures.

set -u
cd "$(dirname "$0")"

: > _failed.txt
: > _success.txt

clone_one() {
  local slug="$1"
  local owner="${slug%/*}"
  local name="${slug#*/}"
  local dest="${owner}__${name}"

  if [ -d "$dest" ]; then
    echo "SKIP $slug (exists)"
    echo "$slug" >> _success.txt
    return 0
  fi

  if git clone --depth 1 --quiet "https://github.com/${slug}.git" "$dest" 2>/dev/null; then
    rm -rf "${dest}/.git"
    echo "OK   $slug"
    echo "$slug" >> _success.txt
  else
    echo "FAIL $slug"
    echo "$slug" >> _failed.txt
    rm -rf "$dest" 2>/dev/null
  fi
}

export -f clone_one

# Parallel xargs: 8 concurrent clones (gentle on GitHub rate limit)
grep -v '^[[:space:]]*$' _repos.txt | grep -v '^#' \
  | xargs -P 8 -I {} bash -c 'clone_one "$@"' _ {}

echo ""
echo "=========================================="
echo "Success: $(wc -l < _success.txt) repos"
echo "Failed:  $(wc -l < _failed.txt) repos"
echo "=========================================="
if [ -s _failed.txt ]; then
  echo "Failures:"
  cat _failed.txt
fi
