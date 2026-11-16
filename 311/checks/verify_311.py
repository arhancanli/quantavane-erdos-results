"""Independent check for the delta(N) table (Erdos #311), exact rational arithmetic (fractions).
Reads program A's output (with one optimal set per N) and program B's output (delta only).
Checks for each N: (1) the set lies in {1..N}; (2) |1 - sum 1/a| over the set equals A's delta and is nonzero;
(3) A's delta equals B's delta; (4) delta(N) <= delta(N-1); (5) the N <= 25 values equal the published table (as listed on the plasma-ai/erdos page E0311);
(6) A's output covers every N from 1 to its largest N.
Exits non-zero on any failure. Usage: python3 verify_311.py A.txt B.txt"""
import sys, re
from fractions import Fraction as F
TABLE25 = ['1','1/2','1/6','1/12','1/30','1/30','1/105','1/120','1/252','1/360','1/2310','1/2310','1/2310',
           '1/2772','1/2772','1/6160','1/30940','1/30940','5/298452','5/298452','11/1244880','23/17907120',
           '1/1105104','1/1105104','1/1593900']
def parse(path, want_set):
    out = {}
    for line in open(path):
        m = re.match(r'N=(\d+) delta=(\d+)/(\d+)', line)
        if not m: continue
        N = int(m.group(1)); d = F(int(m.group(2)), int(m.group(3)))
        s = None
        if want_set:
            ms = re.search(r'set=([\d,]*)', line); s = [int(x) for x in ms.group(1).split(',') if x]
        out[N] = (d, s)
    return out
A = parse(sys.argv[1], True); B = parse(sys.argv[2], False)
bad = 0; prev = None
if sorted(A) != list(range(1, max(A) + 1)):
    print('FAIL: program A output does not cover every N from 1 to', max(A)); bad += 1
for N in sorted(A):
    d, s = A[N]
    ok = all(1 <= a <= N for a in s) and len(set(s)) == len(s)
    val = abs(1 - sum((F(1, a) for a in s), F(0)))
    ok = ok and val == d and d != 0
    ok = ok and N in B and B[N][0] == d
    if prev is not None: ok = ok and d <= prev
    if N <= 25: ok = ok and d == F(TABLE25[N - 1])
    if not ok: bad += 1; print('FAIL', N, d, s, val, B.get(N))
    prev = d
print(f'checked {len(A)} values; failures {bad}; B-only values: {sorted(set(B) - set(A))}')
sys.exit(1 if bad else 0)
