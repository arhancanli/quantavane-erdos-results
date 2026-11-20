# Program C (small n): enumerate every pairwise coprime subset of [1, n) recursively, exact fractions.
import sys, math
from fractions import Fraction
def M(n):
    best = Fraction(0)
    def rec(i, chosen, val):
        nonlocal best
        if val > best: best = val
        for a in range(i, n):
            if all(math.gcd(a, b) == 1 for b in chosen): rec(a + 1, chosen + [a], val + Fraction(1, n - a))
    rec(1, [], Fraction(0)); return best
for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1): print('n=%d M=%s' % (n, M(n))); sys.stdout.flush()
