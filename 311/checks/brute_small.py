"""Third check for #311 at small N: plain enumeration of all 2^N subsets (no meet in the middle), exact integers."""
import sys, math
from fractions import Fraction as F
res = {}
for N in range(1, int(sys.argv[1]) + 1):
    L = 1
    for a in range(1, N + 1): L = L * a // math.gcd(L, a)
    w = [L // a for a in range(1, N + 1)]
    sums = [0]
    for x in w: sums += [s + x for s in sums]
    best = min(abs(L - s) for s in sums if s != L)
    res[N] = F(best, L)
    print(f"N={N} delta={res[N].numerator}/{res[N].denominator}")
