#!/bin/sh
# Re-checks this repository.   sh checks/run_checks.sh [--quick | --full]
#   --quick (default): Python 3 standard library only, about a minute.
#     #160: both checkers accept the 77-colouring (and the published 76-colouring) and both reject every red control.
#     #311: the exact verifier accepts the two programs' outputs and rejects every red control; plain brute force
#           agrees for N <= 16.
#     #902: the 17 group tables are groups with the recorded invariants; the brute-force S_4 checker accepts the
#           Paley tournament on 67 vertices and rejects the one on 59 and the red controls; every group in both
#           sweep logs has pass=0 (Z_67 control: pass=2).
#   --full: also compiles the C programs (cc) and reruns: #311 programs A and B for N <= 40 against the stored values;
#           #902 the three programs on Z_47, Z_7 x Z_7 and Z_11 x| Z_5, and the S_3 counts for n = 25..33 (all
#           programs must agree); #160 the Lean file if `lean` (v4.35.0) is on the PATH. A few minutes.
#   #461, #535, #624, #982, #1159, #1210: each folder's own checks/run.sh, in the same mode (see the folders' READMEs).
# The last line is "ALL PASS" only if every check passed.
cd "$(dirname "$0")/.." || exit 1
mode=${1:---quick}
fail=0
ok()  { echo "ok   $*"; }
bad() { echo "FAIL $*"; fail=1; }
expect_pass() { d="$1"; shift; if "$@" > /dev/null 2>&1; then ok "$d"; else bad "$d"; fi; }
expect_fail() { d="$1"; shift; if "$@" > /dev/null 2>&1; then bad "$d (accepted a red control)"; else ok "$d (refused)"; fi; }

echo "== #160"
expect_pass "check160 k7_N77" python3 -I 160/checks/check160.py 160/witness/k7_N77.txt 7
expect_pass "check160_cnf k7_N77" python3 -I 160/checks/check160_cnf.py 160/witness/k7_N77.txt 7
expect_pass "check160 published k7_N76" python3 -I 160/checks/check160.py 160/witness/k7_N76_from_scottschluer.txt 7
expect_pass "check160_cnf published k7_N76" python3 -I 160/checks/check160_cnf.py 160/witness/k7_N76_from_scottschluer.txt 7
for f in 160/controls/red_*.txt; do
  expect_fail "check160 $f" python3 -I 160/checks/check160.py "$f" 7
  expect_fail "check160_cnf $f" python3 -I 160/checks/check160_cnf.py "$f" 7
done
[ "$(wc -w < 160/witness/k7_N77.txt | tr -d ' ')" = 77 ] && ok "witness has 77 entries" || bad "witness length"

echo "== #311"
expect_pass "verify_311 A vs B, N <= 60" python3 -I 311/checks/verify_311.py 311/results/A_1_60.txt 311/results/B_1_60.txt
for f in 311/controls/red_*.txt; do expect_fail "verify_311 $f" python3 -I 311/checks/verify_311.py "$f" 311/results/B_1_60.txt; done
python3 -I 311/checks/brute_small.py 16 > /tmp/qv311_brute.$$ 2>/dev/null
if [ "$(cut -d' ' -f1,2 /tmp/qv311_brute.$$)" = "$(head -16 311/results/A_1_60.txt | cut -d' ' -f1,2)" ]; then ok "brute force = A for N <= 16"; else bad "brute force differs from A"; fi
rm -f /tmp/qv311_brute.$$

echo "== #902"
python3 -I 902/checks/group_invariants.py 902/groups/group_*.txt > /tmp/qv902_inv.$$ 2>&1
if cmp -s /tmp/qv902_inv.$$ 902/checks/group_invariants.expected; then ok "17 group tables: axioms and invariants"; else bad "group tables"; fi
rm -f /tmp/qv902_inv.$$
expect_pass "check_sk Paley 67 has S_4" python3 -I 902/checks/check_sk.py 902/controls/paley67.txt 4
expect_fail "check_sk Paley 59" python3 -I 902/checks/check_sk.py 902/controls/paley59.txt 4
expect_fail "check_sk Paley 67 with one arc reversed" python3 -I 902/checks/check_sk.py 902/controls/paley67_one_arc_reversed.txt 4
expect_fail "check_sk not a tournament" python3 -I 902/checks/check_sk.py 902/controls/red_not_tournament.txt 3
for g in Zc47 Zc49 Z7xZ7 Zc51 Zc53 Zc55 Z11sZ5 Zc57 Z19sZ3 Zc59 Zc61 Zc63 Z3xZ21 Z7sZ9 Z3xZ7sZ3 Zc65; do
  grep -q "^$g SUMMARY .* k=4 .* pass=0 " 902/results/cayley.log && grep -q "^$g SUMMARY_A .* pass=0 " 902/results/direct.log \
    && ok "$g: pass=0 in both sweep logs" || bad "$g: sweep logs"
done
grep -q "^Zc67 SUMMARY .* pass=2 " 902/results/cayley.log && grep -q "^A n=67 DONE .* hits=2 " 902/results/cayley.log \
  && ok "Z_67 control: exactly 2 S_4 circulants in both programs" || bad "Z_67 control"
for n in 47 49 51 53 55 57 59 61 63 65; do grep -q "^DONE n=$n k=4 .* hits=0" 902/results/circ_sweep.log && ok "circ_s4 n=$n: none" || bad "circ_s4 n=$n"; done

if [ "$mode" = --full ]; then
  tmp=$(mktemp -d)
  echo "== compile"
  for p in 311/src/delta_stream_a 311/src/delta_merge_b 902/src/circ_s4 902/src/cayley_sk128 902/src/cayley_direct; do
    cc -O3 -o "$tmp/$(basename $p)" "$p.c" && ok "cc $p.c" || bad "cc $p.c"
  done
  echo "== #311 rerun N <= 40"
  for N in $(seq 1 40); do "$tmp/delta_stream_a" $N; done > "$tmp/A.txt"
  for N in $(seq 1 40); do "$tmp/delta_merge_b" $N; done > "$tmp/B.txt"
  [ "$(cut -d' ' -f1,2 "$tmp/A.txt")" = "$(head -40 311/results/A_1_60.txt | cut -d' ' -f1,2)" ] && ok "A rerun = stored" || bad "A rerun"
  [ "$(cut -d' ' -f1,2 "$tmp/B.txt")" = "$(head -40 311/results/B_1_60.txt | cut -d' ' -f1,2)" ] && ok "B rerun = stored" || bad "B rerun"
  echo "== #902 reruns"
  "$tmp/circ_s4" 47 4 | tail -1 | grep -q "hits=0$" && ok "circ_s4 n=47: none" || bad "circ_s4 47"
  for g in Zc47 Z7xZ7 Z11sZ5; do
    "$tmp/cayley_sk128" 902/groups/group_$g.txt 4 | tail -1 | grep -q "pass=0$" && ok "cayley_sk128 $g: none" || bad "cayley_sk128 $g"
    "$tmp/cayley_direct" 902/groups/group_$g.txt | tail -1 | grep -q "pass=0$" && ok "cayley_direct $g: none" || bad "cayley_direct $g"
  done
  for n in 25 27 29 31 33; do
    python3 -I 902/src/make_groups.py "$tmp" Zc$n > /dev/null
    a=$("$tmp/circ_s4" $n 3 | tail -1 | sed 's/.*hits=//'); b=$("$tmp/cayley_sk128" "$tmp/group_Zc$n.txt" 3 | tail -1 | sed 's/.*pass=//')
    [ -n "$a" ] && [ "$a" = "$b" ] && ok "S_3 circulants n=$n: $a in both" || bad "S_3 counts n=$n ($a vs $b)"
  done
  echo "== #160 Lean"
  if command -v lean > /dev/null 2>&1; then
    out=$(cd 160/lean && printf '%s\n' "$(cat Erdos160H77.lean)" "#print axioms every_4AP_three_colours" > "$tmp/L.lean" && lean "$tmp/L.lean" 2>&1)
    echo "$out" | grep -q "depends on axioms: \[propext\]" && ! echo "$out" | grep -q error && ok "Lean: decide, axioms [propext]" || bad "Lean"
  else echo "skip Lean (no lean on PATH)"; fi
  rm -rf "$tmp"
fi
for p in 461 535 624 982 1159 1210; do
  sh "$p/checks/run.sh" "$mode" > /tmp/qv_erdos_$p.$$ 2>&1
  r=$?; grep -v '^ok ' /tmp/qv_erdos_$p.$$ | grep -v '^== '; grep -c '^ok ' /tmp/qv_erdos_$p.$$ | sed "s/^/ok   #$p: /; s/\$/ checks passed/"
  [ $r = 0 ] || fail=1
  rm -f /tmp/qv_erdos_$p.$$
done
if [ $fail = 0 ]; then echo "ALL PASS"; else echo "SOME CHECK FAILED"; exit 1; fi
