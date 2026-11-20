#!/bin/sh
# Re-checks Erdős #1159.   sh 1159/checks/run.sh [--quick | --full]
#   Both checkers (Python 3 standard library, about ten seconds) rebuild each of the twelve planes, check that it is a
#   projective plane of order q, check that every line meets the listed set in 1..C points, and show that no set can
#   do this with C - 1 (checker A by the quadratic counting inequality, checker B by the integer line-type equations).
#   Red controls (a point removed, a cap claimed one too small, a reducible field modulus, a plane file with two points
#   swapped) must be refused by both. --full is the same as --quick here.
# The last line is "ALL PASS" only if every check passed.
cd "$(dirname "$0")/.." || exit 1
fail=0
ok()  { echo "ok   $*"; }
bad() { echo "FAIL $*"; fail=1; }

echo "== #1159"
for c in a b; do
  n=$(python3 -I checks/check1159_$c.py results/witnesses.json | grep -c '^PASS')
  [ "$n" = 12 ] && python3 -I checks/check1159_$c.py results/witnesses.json > /dev/null \
    && ok "check1159_$c: all 12 planes pass (set meets every line in 1..C points; C - 1 impossible)" || bad "check1159_$c: $n of 12"
done
for r in controls/red_*.json; do
  python3 -I checks/check1159_a.py "$r" > /dev/null 2>&1 && bad "check1159_a accepted $r" || ok "check1159_a refuses $r"
  python3 -I checks/check1159_b.py "$r" > /dev/null 2>&1 && bad "check1159_b accepted $r" || ok "check1159_b refuses $r"
done
if [ $fail = 0 ]; then echo "ALL PASS (#1159)"; else echo "SOME CHECK FAILED (#1159)"; exit 1; fi
