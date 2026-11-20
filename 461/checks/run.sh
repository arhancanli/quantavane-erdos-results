#!/bin/sh
# Re-checks Erdős #461.   sh 461/checks/run.sh [--quick | --full]
#   --quick (default, Python 3 standard library, a few seconds):
#     both CRT checkers rebuild n from every witness and count the distinct s_t(n+1), ..., s_t(n+t) from the definition
#     (t = 2..64 and t = 160, 640, 1280, 2560); each count must equal the table; the exhaustive Python search
#     (src/dfs461.py) must give the table for t <= 26 and the brute force over all n mod M_t for t <= 9;
#     red controls (a changed residue, a search without the prime 2) must disagree with the table.
#   --full: also compiles and reruns the C searches: src/bnb461.c for t <= 46, the referee's checks/referee_min461.c for
#     t <= 52 and checks/referee_brute461.c for t <= 11, each against the table; red: the over-eager prune and the
#     referee's cap-1 variant must disagree. About a minute.
# The last line is "ALL PASS" only if every check passed.
cd "$(dirname "$0")/.." || exit 1
mode=${1:---quick}
fail=0
ok()  { echo "ok   $*"; }
bad() { echo "FAIL $*"; fail=1; }
want() { awk -v t="$1" '$1 == t { print $2 }' results/table.txt; }

echo "== #461 witnesses (two CRT checkers, counts from the definition)"
nw=0
while read -r t f rest; do
  case "$t" in ''|\#*) continue ;; esac
  a=$(python3 -I checks/check461_crt.py "$t" $rest | sed -n 's/.*distinct=\([0-9]*\).*/\1/p')
  b=$(python3 -I checks/check461_crt_b.py "$t" neg $rest | sed -n 's/.*distinct s_t(n+1..n+t) = \([0-9]*\).*/\1/p')
  if [ "$a" = "$f" ] && [ "$b" = "$f" ] && [ "$(want "$t")" = "$f" ]; then nw=$((nw + 1)); else bad "witness t=$t: checkers $a / $b, claimed $f, table $(want "$t")"; fi
done < results/witnesses.txt
[ "$nw" = 63 ] && ok "t = 2..64: both checkers count exactly the table value at all 63 witnesses" || bad "only $nw of 63 witnesses passed"
while read -r t f rest; do
  case "$t" in ''|\#*) continue ;; esac
  a=$(python3 -I checks/check461_crt.py "$t" $rest | sed -n 's/.*distinct=\([0-9]*\).*/\1/p')
  b=$(python3 -I checks/check461_crt_b.py "$t" neg $rest | sed -n 's/.*distinct s_t(n+1..n+t) = \([0-9]*\).*/\1/p')
  [ "$a" = "$f" ] && [ "$b" = "$f" ] && ok "t=$t: f(n,t) = $f for the listed n (both checkers)" || bad "large t=$t: $a / $b, claimed $f"
done < results/witnesses_large.txt

echo "== #461 minimality, small t (exhaustive searches against the table)"
m=0
for t in $(seq 2 26); do
  v=$(python3 -I src/dfs461.py "$t" | sed -n 's/.*min_f=\([0-9]*\).*/\1/p'); [ "$v" = "$(want "$t")" ] && m=$((m + 1)) || bad "dfs461 t=$t gives $v"
done
[ "$m" = 25 ] && ok "src/dfs461.py = table for t = 2..26"
m=0
for t in 2 3 4 5 6 7 8 9; do
  v=$(python3 -I src/brute461.py "$t" | sed -n 's/.*min_f=\([0-9]*\).*/\1/p'); [ "$v" = "$(want "$t")" ] && m=$((m + 1)) || bad "brute461 t=$t gives $v"
done
[ "$m" = 8 ] && ok "src/brute461.py (every n mod M_t, from the definition) = table for t = 2..9"

echo "== #461 red controls"
while read -r t f rest; do
  case "$t" in ''|\#*) continue ;; esac
  a=$(python3 -I checks/check461_crt.py "$t" $rest | sed -n 's/.*distinct=\([0-9]*\).*/\1/p')
  b=$(python3 -I checks/check461_crt_b.py "$t" neg $rest | sed -n 's/.*distinct s_t(n+1..n+t) = \([0-9]*\).*/\1/p')
  [ "$a" != "$f" ] && [ "$b" != "$f" ] && ok "changed residue at t=$t: both checkers count $a, not $f (refused)" || bad "red witness accepted"
done < controls/red_witness_t44.txt
for t in 10 16 20; do
  v=$(python3 -I controls/red_dfs_drop2.py "$t" | sed -n 's/.*min_f=\([0-9]*\).*/\1/p')
  [ "$v" != "$(want "$t")" ] && ok "search without the prime 2, t=$t: $v, not $(want "$t") (refused)" || bad "red dfs t=$t agrees with the table"
done

if [ "$mode" = --full ]; then
  tmp=$(mktemp -d)
  echo "== #461 compile"
  for p in src/bnb461 checks/referee_min461 checks/referee_brute461 controls/red_bnb_prune; do
    cc -O2 -o "$tmp/$(basename $p)" "$p.c" 2>/dev/null && ok "cc $p.c" || bad "cc $p.c"
  done
  m=0; for t in $(seq 2 46); do
    v=$("$tmp/bnb461" "$t" | sed -n 's/.*min_f=\([0-9]*\).*/\1/p'); [ "$v" = "$(want "$t")" ] && m=$((m + 1)) || bad "bnb461 t=$t gives $v"
  done; [ "$m" = 45 ] && ok "src/bnb461.c = table for t = 2..46"
  m=0; for t in $(seq 2 52); do
    v=$("$tmp/referee_min461" "$t" a | head -1 | sed -n 's/.*min_f=\([0-9]*\).*/\1/p'); [ "$v" = "$(want "$t")" ] && m=$((m + 1)) || bad "referee_min461 t=$t gives $v"
  done; [ "$m" = 51 ] && ok "checks/referee_min461.c = table for t = 2..52"
  m=0; for t in $(seq 2 11); do
    v=$("$tmp/referee_brute461" "$t" | tail -1 | sed -n 's/.*min_f=\([0-9]*\).*/\1/p'); [ "$v" = "$(want "$t")" ] && m=$((m + 1)) || bad "referee_brute461 t=$t gives $v"
  done; [ "$m" = 10 ] && ok "checks/referee_brute461.c (every n mod M_t) = table for t = 2..11"
  for t in 10 30; do
    v=$("$tmp/red_bnb_prune" "$t" | sed -n 's/.*min_f=\([0-9]*\).*/\1/p'); [ "$v" != "$(want "$t")" ] && ok "over-eager prune, t=$t: $v (refused)" || bad "red prune t=$t agrees"
  done
  for t in 12 24 44; do
    v=$("$tmp/referee_min461" "$t" a $((t + 1)) 0 5 | head -1 | sed -n 's/.*min_f=\([0-9]*\).*/\1/p'); [ "$v" != "$(want "$t")" ] && ok "cap-1 variant, t=$t: $v (refused)" || bad "red cap-1 t=$t agrees"
  done
  rm -rf "$tmp"
fi
if [ $fail = 0 ]; then echo "ALL PASS (#461)"; else echo "SOME CHECK FAILED (#461)"; exit 1; fi
