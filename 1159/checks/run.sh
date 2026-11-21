#!/bin/sh
# Re-checks Erdős #1159.   sh 1159/checks/run.sh [--quick | --full]
#   Both checkers (Python 3 standard library, about ten seconds) rebuild each of the twelve planes, check that it is a
#   projective plane of order q, check that every line meets the listed set in 1..C points, and show that no set can
#   do this with C - 1 (checker A by the quadratic counting inequality, checker B by the integer line-type equations).
#   Red controls (a point removed, a cap claimed one too small, a reducible field modulus, a plane file with two points
#   swapped) must be refused by both.
#   --full also runs the referee's programs: its own witness check (with two sets of field polynomials), its
#   exhaustive searches (no cap-3 set in PG(2,5) and PG(2,7), least cap 3 for q <= 4) and its Baer subplanes.
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
if [ "$1" = "--full" ]; then
  for alt in "" --alt; do
    python3 -I checks/referee_witnesses.py results/witnesses.json $alt > /dev/null \
      && ok "referee_witnesses $alt: all 12 sets pass in the referee's own planes" || bad "referee_witnesses $alt"
  done
  python3 -I checks/referee_baer.py planes > /dev/null && ok "referee_baer: a Baer subplane in each plane of order 9" \
    || bad "referee_baer"
  tmp=$(mktemp -d) || exit 1
  if cc -O2 -o "$tmp/exh" checks/referee_exh.c && cc -O2 -o "$tmp/brute" checks/referee_brute.c; then
    python3 -I checks/referee_exhaustive.py "$tmp/exh" "$tmp/brute" --with-q5-brute \
      && ok "referee_exhaustive: no cap-3 set in PG(2,5), PG(2,7); least cap 3 for q <= 4" || bad "referee_exhaustive"
  else
    bad "could not compile the referee's C programs"
  fi
  rm -rf "$tmp"
fi
if [ $fail = 0 ]; then echo "ALL PASS (#1159)"; else echo "SOME CHECK FAILED (#1159)"; exit 1; fi
