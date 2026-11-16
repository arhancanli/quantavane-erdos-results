"""Independent checker for Erdos #160 colourings: reads whitespace-separated colours c(1..N), checks every 4-term AP
a, a+d, a+2d, a+3d in [1, N] has at least 3 distinct colours, reports N, number of colours used and of APs checked.
Usage: python3 check160.py file [k]"""
import sys
c = [int(t) for t in open(sys.argv[1]).read().split()]
N = len(c); used = sorted(set(c)); k = int(sys.argv[2]) if len(sys.argv) > 2 else len(used)
if len(used) > k: print(f'FAIL uses {len(used)} colours > {k}'); sys.exit(1)
bad = []; n_ap = 0
for a in range(N):
    d = 1
    while a + 3 * d < N:
        n_ap += 1
        if len({c[a], c[a + d], c[a + 2 * d], c[a + 3 * d]}) < 3: bad.append((a + 1, d))
        d += 1
if bad: print(f'FAIL N={N}: {len(bad)} bad APs, first (start, step) = {bad[0]}'); sys.exit(1)
print(f'PASS N={N}, colours used {len(used)} (<= {k}), all {n_ap} 4-APs have >= 3 colours')
