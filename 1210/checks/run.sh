#!/bin/sh
# Re-checks Erdős #1210.   sh 1210/checks/run.sh [--quick | --full | --all]
#   --quick (default, Python 3 standard library, under half a minute): check1210.py verifies every listed maximiser
#     (pairwise coprime, exact value M(n), E(n)) for n = 3..1794; the referee's exact dynamic programme
#     (checks/dp1210_referee.py, a different algorithm) recomputes M(n) for n <= 300, the original branch and bound
#     (src/bnb1210.py) for n <= 300 and full enumeration (src/brute1210.py) for n <= 24, all against the table;
#     red controls (a non-coprime set, a wrong value, the dynamic programme with the prime 2 ignored) are refused.
#   --full: the dynamic programme also for n <= 1000 and for every 50th n up to 1794 (a few minutes).
#   --all: the dynamic programme for every n = 3..1794 (about half an hour on one core).
# The last line is "ALL PASS" only if every check passed.
cd "$(dirname "$0")/.." || exit 1
mode=${1:---quick}
fail=0
ok()  { echo "ok   $*"; }
bad() { echo "FAIL $*"; fail=1; }
tmp=$(mktemp -d)
dp() { python3 -I checks/dp1210_referee.py results/table.txt "$@" | tail -1 | sed -n 's/^rows not agreeing or with bad set: //p'; }

echo "== #1210"
python3 -I checks/check1210.py results/table.txt > /dev/null && ok "check1210: all 1,792 maximisers (n = 3..1794) pairwise coprime with value exactly M(n)" || bad "check1210"
[ "$(dp 3 300)" = 0 ] && ok "dp1210_referee (exact DP over small primes) = table for n = 3..300" || bad "dp1210_referee n <= 300"
python3 -I src/bnb1210.py 3 300 > "$tmp/b.txt"
python3 -I checks/compare1210.py results/table.txt "$tmp/b.txt" > /dev/null && ok "src/bnb1210.py rerun = table for n = 3..300" || bad "bnb1210 rerun"
python3 -I src/brute1210.py 3 24 > "$tmp/c.txt"
python3 -I checks/compare1210.py results/table.txt "$tmp/c.txt" > /dev/null && ok "src/brute1210.py (every pairwise coprime set) = table for n = 3..24" || bad "brute1210"
python3 -I checks/check1210.py controls/red_not_coprime.txt > /dev/null 2>&1 && bad "accepted a non-coprime set" || ok "check1210 refuses red_not_coprime"
python3 -I checks/check1210.py controls/red_value.txt > /dev/null 2>&1 && bad "accepted a wrong value" || ok "check1210 refuses red_value"
r=$(python3 -I checks/dp1210_referee.py results/table.txt 3 40 --red | tail -1 | sed -n 's/^rows not agreeing or with bad set: //p')
[ -n "$r" ] && [ "$r" -gt 0 ] && ok "dynamic programme with the prime 2 ignored: $r of 38 rows flagged (refused)" || bad "red DP not flagged"

if [ "$mode" = --full ]; then
  [ "$(dp 301 1000)" = 0 ] && ok "dp1210_referee = table for n = 301..1000" || bad "dp1210_referee n = 301..1000"
  s=0; for n in $(seq 1050 50 1750) 1794; do [ "$(dp "$n" "$n")" = 0 ] && s=$((s + 1)) || bad "dp1210_referee n=$n"; done
  [ "$s" = 16 ] && ok "dp1210_referee = table at n = 1050, 1100, ..., 1750 and 1794" || bad "dp1210_referee samples ($s of 16)"
fi
if [ "$mode" = --all ]; then
  [ "$(dp 301 1794)" = 0 ] && ok "dp1210_referee = table for every n = 301..1794" || bad "dp1210_referee n = 301..1794"
fi
rm -rf "$tmp"
if [ $fail = 0 ]; then echo "ALL PASS (#1210)"; else echo "SOME CHECK FAILED (#1210)"; exit 1; fi
