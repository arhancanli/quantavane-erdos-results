#!/bin/sh
# Re-checks Erdős #535.   sh 535/checks/run.sh [--quick | --full]
#   --quick (default, Python 3 standard library, a few seconds): the two set checkers (definition; structure lemma)
#     accept every optimal set of the table; the exhaustive search checks/search535.py re-derives f_3(N) for every
#     N <= 64 and must agree; red controls (a set with a forbidden triple; a table with three values lowered) are refused.
#   --full: also compiles the referee's solver-free branch and bound (checks/referee_535_bnb.c) and compares it for
#     every N <= 64 (under a second).
# The last line is "ALL PASS" only if every check passed.
cd "$(dirname "$0")/.." || exit 1
mode=${1:---quick}
fail=0
ok()  { echo "ok   $*"; }
bad() { echo "FAIL $*"; fail=1; }
tmp=$(mktemp -d)

echo "== #535"
python3 -I checks/check535.py results/table.txt > /dev/null && ok "check535 (definition): all 64 optimal sets valid" || bad "check535"
python3 -I checks/check535_b.py results/table.txt > /dev/null && ok "check535_b (structure lemma): all 64 optimal sets valid" || bad "check535_b"
python3 -I checks/search535.py 1 64 > "$tmp/search.txt"
python3 -I checks/check535.py results/table.txt "$tmp/search.txt" > /dev/null && ok "search535 (exhaustive) = table for every N = 1..64" || bad "search535 differs from the table"
python3 -I checks/check535.py "$tmp/search.txt" > /dev/null && ok "the search's own sets pass check535" || bad "search sets"
python3 -I checks/check535.py controls/red_forbidden_triple.txt > /dev/null 2>&1 && bad "check535 accepted a forbidden triple" || ok "check535 refuses red_forbidden_triple"
python3 -I checks/check535_b.py controls/red_forbidden_triple.txt > /dev/null 2>&1 && bad "check535_b accepted a forbidden triple" || ok "check535_b refuses red_forbidden_triple"
head -20 "$tmp/search.txt" > "$tmp/s20.txt"
python3 -I checks/check535.py controls/red_lowered.txt "$tmp/s20.txt" > /dev/null 2>&1 && bad "lowered table accepted" || ok "lowered values at N = 18..20 refused by the comparison with the search"

if [ "$mode" = --full ]; then
  cc -O2 -o "$tmp/referee_535_bnb" checks/referee_535_bnb.c 2>/dev/null && ok "cc checks/referee_535_bnb.c" || bad "cc referee_535_bnb.c"
  "$tmp/referee_535_bnb" 1 64 | sed -n 's/^N=\([0-9]*\) f=\([0-9]*\) check=ok set=\(.*\)/\1 \2 \3/p' > "$tmp/ref.txt"
  [ "$(wc -l < "$tmp/ref.txt" | tr -d ' ')" = 64 ] && python3 -I checks/check535.py results/table.txt "$tmp/ref.txt" > /dev/null \
    && python3 -I checks/check535.py "$tmp/ref.txt" > /dev/null && ok "referee_535_bnb = table for every N = 1..64 (its sets valid)" || bad "referee_535_bnb"
fi
rm -rf "$tmp"
if [ $fail = 0 ]; then echo "ALL PASS (#535)"; else echo "SOME CHECK FAILED (#535)"; exit 1; fi
