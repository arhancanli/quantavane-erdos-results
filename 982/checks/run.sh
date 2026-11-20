#!/bin/sh
# Re-checks the parts of the Erdős #982 proof (n <= 13) that can be checked without Lean.   sh 982/checks/run.sh [--quick | --full]
# The full proof is the Lean 4 project arhancanli/quantavane-lean (commit 19426bf), checked by Lean; see 982/README.md.
#   --quick (default, Python 3 standard library, a few seconds):
#     the four CNFs are byte for byte the ones Lean's `lake exe dumpc n K` writes (SHA-256 below); the LRAT proofs that
#     Lean checks with native_decide for n = 4, 6, 8, 10 pass checks/lrat_check.py; the n = 12 angle certificate passes
#     check_angle12.py (exact rational arithmetic, all 24 dihedral images) and the 24 cut images pass check_cuts12.py;
#     red controls (a truncated proof, a proof with one hint removed, a doubled multiplier, a repeated image) are refused.
#   --full: also compiles our C LRAT checker (checks/lratcheck.c) and checks the four proofs with it.
# The last line is "ALL PASS" only if every check passed.
cd "$(dirname "$0")/.." || exit 1
mode=${1:---quick}
fail=0
ok()  { echo "ok   $*"; }
bad() { echo "FAIL $*"; fail=1; }
tmp=$(mktemp -d)
D=certificates/lrat
sha() { python3 -I -c "import gzip,hashlib,sys; p=sys.argv[1]; f=gzip.open(p) if p.endswith('.gz') else open(p,'rb'); print(hashlib.sha256(f.read()).hexdigest())" "$1"; }

echo "== #982"
for row in "4_1 6d8f246ff2f1e6f54792cb14b4a92e25e78789facd023c94d7ee70e3c1740f04 gen_4_1.cnf" \
           "6_2 325644d4c7088a40cb23bd0efa3eee316ffac14b650c758719f6f9ea0f13ab61 gen_6_2.cnf" \
           "8_3 fa59400aed096db379b3a560993b87aace39998c4d354693ef0596c2538dd398 gen_8_3.cnf" \
           "10_4 92b4ad698357b7e97b652dce53ac5b2516c0471ef0131a6690ee8c74490c1999 gen_10_4.cnf.gz"; do
  set -- $row
  [ "$(sha $D/$3)" = "$2" ] && ok "gen $1: CNF SHA-256 ${2%"${2#????????}"}... (as written by Lean's dumpc)" || bad "gen $1: CNF hash"
  p=$D/gen_$1.lrat; [ -f "$p" ] || p=$p.gz
  python3 -I ../checks/lrat_check.py $D/$3 "$p" | grep -q '^s VERIFIED UNSAT' && ok "gen $1: LRAT refutation verified (lrat_check.py)" || bad "gen $1: LRAT"
done
out=$(python3 -I checks/check_angle12.py certificates/core1.cert)
echo "$out" | grep -q 'margin = 45 PASS' && echo "$out" | grep -q 'passing: 24 of 24' \
  && ok "n = 12 angle certificate: weighted sum gives a contradiction of 45 degrees; all 24 dihedral images pass" || bad "angle certificate"
echo "$out" | grep -q 'red control (one hypothesis removed): FAIL as expected' && ok "angle certificate with one equality removed is refused" || bad "angle red control"
python3 -I checks/check_cuts12.py certificates/cuts12_images.json > /dev/null && ok "cuts12_images.json: exactly the 24 dihedral images" || bad "cuts12"
python3 -I ../checks/lrat_check.py $D/gen_8_3.cnf controls/red_gen_8_3_truncated.lrat | grep -q '^s VERIFIED' && bad "truncated proof accepted" || ok "lrat_check refuses red_gen_8_3_truncated"
python3 -I ../checks/lrat_check.py $D/gen_8_3.cnf controls/red_gen_8_3_hint_dropped.lrat | grep -q '^s VERIFIED' && bad "hint-dropped proof accepted" || ok "lrat_check refuses red_gen_8_3_hint_dropped"
python3 -I checks/check_angle12.py controls/red_core1_multiplier_doubled.cert | grep -q 'PASS' && bad "doubled multiplier accepted" || ok "check_angle12 refuses red_core1_multiplier_doubled"
python3 -I checks/check_cuts12.py controls/red_cuts12_one_image_repeated.json > /dev/null && bad "repeated image accepted" || ok "check_cuts12 refuses red_cuts12_one_image_repeated"

if [ "$mode" = --full ]; then
  cc -O2 -o "$tmp/lratcheck" ../checks/lratcheck.c 2>/dev/null && ok "cc checks/lratcheck.c" || bad "cc lratcheck.c"
  for k in 4_1 6_2 8_3 10_4; do
    for x in cnf lrat; do
      if [ -f $D/gen_$k.$x ]; then cp $D/gen_$k.$x "$tmp/g.$x"
      else python3 -I -c "import gzip,sys; sys.stdout.buffer.write(gzip.open(sys.argv[1]).read())" $D/gen_$k.$x.gz > "$tmp/g.$x"; fi
    done
    "$tmp/lratcheck" "$tmp/g.cnf" "$tmp/g.lrat" 2>/dev/null | grep -q '^s VERIFIED UNSAT' && ok "lratcheck: gen $k verified" || bad "lratcheck gen $k"
  done
  "$tmp/lratcheck" $D/gen_8_3.cnf controls/red_gen_8_3_hint_dropped.lrat 2>/dev/null | grep -q '^s VERIFIED UNSAT' && bad "lratcheck accepted the red proof" || ok "lratcheck refuses red_gen_8_3_hint_dropped"
fi
rm -rf "$tmp"
if [ $fail = 0 ]; then echo "ALL PASS (#982)"; else echo "SOME CHECK FAILED (#982)"; exit 1; fi
