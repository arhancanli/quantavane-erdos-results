#!/bin/sh
# Re-checks Erdős #624.   sh 624/checks/run.sh [--quick | --full]
#   --quick (default, Python 3 standard library, a few seconds): both witness checkers (check624.py and the referee's
#     check624_ref.py, which tests every Y with |Y| >= h) accept the ten tables f; every "counting" lower bound holds;
#     each certificate CNF is exactly what src/enc624.py writes, and its LRAT proof passes checks/lrat_check.py; the plain
#     search checks/search624.py (no symmetry breaking, no SAT) finds no f for (n, h) = (2,0), (3,1), (4,2), (5,2), (6,2)
#     and finds one for (2,1), (3,2), (4,3); red controls (two corrupted tables, a table used one level too low, a
#     truncated proof) are refused.
#   --full: also compiles our C LRAT checker (checks/lratcheck.c) and checks both proofs with it.
# The last line is "ALL PASS" only if every check passed.
cd "$(dirname "$0")/.." || exit 1
mode=${1:---quick}
fail=0
ok()  { echo "ok   $*"; }
bad() { echo "FAIL $*"; fail=1; }
tmp=$(mktemp -d)
passes() { python3 -I "$@" | tail -1 | grep -q '^PASS'; }

echo "== #624"
prevH=0
while read -r n H d lb w; do
  case "$n" in ''|\#*) continue ;; esac
  passes checks/check624.py "$n" "$H" "results/$w" && passes checks/check624_ref.py "$n" "$H" "results/$w" \
    && ok "n=$n: the listed f works for every Y with |Y| >= $H (both checkers)" || bad "n=$n witness"
  h=$((H - 1))
  case "$lb" in
    counting) [ $((1 << h)) -lt "$n" ] && ok "n=$n: 2^$h < $n, so H($n) > $h" || bad "n=$n counting" ;;
    monotone) [ "$prevH" = "$H" ] && ok "n=$n: H($n) >= H($((n - 1))) = $prevH" || bad "n=$n monotone" ;;
    cert)
      c=results/certificates/e624_n${n}_h${h}.cnf; p=results/certificates/e624_n${n}_h${h}.lrat
      [ -f "$p" ] || p=$p.gz
      python3 -I src/enc624.py "$n" "$h" "$tmp/map.json" --fix0 --prec > "$tmp/e.cnf"
      cmp -s "$tmp/e.cnf" "$c" && ok "n=$n: $c is exactly src/enc624.py's CNF for h = $h" || bad "n=$n CNF differs"
      python3 -I ../checks/lrat_check.py "$c" "$p" | grep -q '^s VERIFIED UNSAT' && ok "n=$n: LRAT proof of unsatisfiability verified (lrat_check.py), so H($n) > $h" || bad "n=$n LRAT" ;;
    *) bad "n=$n: unknown lower-bound kind $lb" ;;
  esac
  prevH=$H
done < results/table.txt
for nh in "2 0" "3 1" "4 2" "5 2" "6 2"; do
  r=$(python3 -I checks/search624.py $nh); [ "${r##* }" = UNSAT ] && ok "search624 (plain search) $nh: no f" || bad "search624 $nh: $r"
done
for nh in "2 1" "3 2" "4 3"; do
  r=$(python3 -I checks/search624.py $nh | cut -d' ' -f3); [ "$r" = SAT ] && ok "search624 (plain search) $nh: f found" || bad "search624 $nh"
done
passes checks/check624.py 7 4 controls/red_n7_value6_to_0.json && bad "check624 accepted red_n7_value6_to_0" || ok "check624 refuses red_n7_value6_to_0"
passes checks/check624_ref.py 7 4 controls/red_n7_value6_to_0.json && bad "check624_ref accepted red_n7_value6_to_0" || ok "check624_ref refuses red_n7_value6_to_0"
passes checks/check624.py 11 4 controls/red_n11_empty_set_changed.json && bad "check624 accepted red_n11" || ok "check624 refuses red_n11_empty_set_changed"
passes checks/check624_ref.py 11 4 controls/red_n11_empty_set_changed.json && bad "check624_ref accepted red_n11" || ok "check624_ref refuses red_n11_empty_set_changed"
passes checks/check624.py 7 3 results/witnesses/f_n7_h4.json && bad "n=7 table accepted at h = 3" || ok "the n=7 table is refused at h = 3"
python3 -I ../checks/lrat_check.py results/certificates/e624_n4_h2.cnf controls/red_e624_n4_h2_truncated.lrat | grep -q '^s VERIFIED' \
  && bad "truncated proof accepted" || ok "lrat_check refuses the truncated proof"

if [ "$mode" = --full ]; then
  cc -O2 -o "$tmp/lratcheck" ../checks/lratcheck.c 2>/dev/null && ok "cc checks/lratcheck.c" || bad "cc lratcheck.c"
  "$tmp/lratcheck" results/certificates/e624_n4_h2.cnf results/certificates/e624_n4_h2.lrat 2>/dev/null | grep -q '^s VERIFIED UNSAT' && ok "lratcheck: (4,2) proof verified" || bad "lratcheck (4,2)"
  python3 -c "import gzip,sys; sys.stdout.write(gzip.open(sys.argv[1],'rt').read())" results/certificates/e624_n7_h3.lrat.gz > "$tmp/p73.lrat"
  "$tmp/lratcheck" results/certificates/e624_n7_h3.cnf "$tmp/p73.lrat" 2>/dev/null | grep -q '^s VERIFIED UNSAT' && ok "lratcheck: (7,3) proof verified" || bad "lratcheck (7,3)"
  "$tmp/lratcheck" results/certificates/e624_n4_h2.cnf controls/red_e624_n4_h2_truncated.lrat 2>/dev/null | grep -q '^s VERIFIED UNSAT' && bad "lratcheck accepted the truncated proof" || ok "lratcheck refuses the truncated proof"
fi
rm -rf "$tmp"
if [ $fail = 0 ]; then echo "ALL PASS (#624)"; else echo "SOME CHECK FAILED (#624)"; exit 1; fi
