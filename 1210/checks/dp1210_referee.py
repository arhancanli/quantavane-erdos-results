# Referee program for #1210 (written without reusing the authors' code).
# M(n) = max over pairwise coprime A subset of [1, n) of sum_{a in A} 1/(n-a).
# Method: exact dynamic programming over subsets of the "small" primes p <= T = isqrt(n-1). Every a < n has at most
# one prime factor q > T (two would give a >= q1*q2 > T^2... precisely q1*q2 >= (T+1)^2 > n-1). Group the candidates:
#   - for each large prime q, the group {a : q | a}: pairwise non-coprime, so at most one is chosen; inside the group
#     only the small-prime support mask matters, so keep the heaviest a per mask;
#   - the T-smooth a >= 2, grouped by exact support mask (same nonzero mask => share a prime => at most one);
#   - a = 1 (mask 0, its own group).
# Two chosen elements from different groups are coprime iff their small masks are disjoint (their large primes
# differ or are absent). So M(n) = max over choices of at most one item per group with pairwise disjoint masks:
# a knapsack over masks. Weights are exact integers L/(n-a), L = lcm(1..n-1); the optimum is reconstructed, checked
# pairwise coprime by gcd, and re-valued with Fractions. No branch and bound, no prime-factor bound, no floats.
# Usage: dp1210_referee.py TABLE n0 n1 [more n0 n1 pairs...] [--red]   (TABLE = results/table.txt; adapted for this
#   repository: the referee's program read a fixed table path, here the path is the first argument)
#   --red: deliberately wrong model that ignores the prime 2 (masks drop bit 0); its sets must FAIL the gcd check.
import sys, math, os, re
from array import array
from fractions import Fraction

def sieve(x):
    s = bytearray([1]) * (x + 1); s[0:2] = b'\x00\x00'
    for i in range(2, math.isqrt(x) + 1):
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(x + 1) if s[i]]

def solve(n, red=False):
    T = math.isqrt(n - 1)
    P = sieve(max(n, 2)); small = [p for p in P if p <= T]; bit = {p: 1 << i for i, p in enumerate(small)}
    L = 1
    for k in range(1, n): L = L * k // math.gcd(L, k)
    groups = {}
    for a in range(1, n):
        x, mask, big = a, 0, None
        for p in small:
            if x % p == 0:
                if not (red and p == 2): mask |= bit[p]
                while x % p == 0: x //= p
        if x > 1: big = x                      # the remaining cofactor is a single prime > T
        key = ('q', big) if big else ('s', mask) if a > 1 else ('one',)
        w = L // (n - a)
        g = groups.setdefault(key, {})
        if mask not in g or w > g[mask][0]: g[mask] = (w, a)
    S = 1 << len(small)
    dp = [-1] * S; dp[0] = 0
    order = list(groups.items()); choices = []
    for key, g in order:
        items = [(m, w, a) for m, (w, a) in g.items()]
        new = dp[:]; ch = array('h', [-1]) * S
        for M in range(S):
            v0 = dp[M]
            if v0 < 0: continue
            for i, (m, w, a) in enumerate(items):
                if M & m: continue
                K = M | m; v = v0 + w
                if v > new[K]: new[K] = v; ch[K] = i
        dp = new; choices.append((items, ch))
    K = max(range(S), key=lambda M: dp[M]); best = dp[K]; A = []
    for items, ch in reversed(choices):
        i = ch[K]
        if i >= 0:
            m, w, a = items[i]; A.append(a); K ^= m
    assert K == 0
    A.sort()
    return Fraction(best, L), A

def claimed(path):
    C = {}
    for line in open(path):
        if line.startswith('#') or not line.strip(): continue
        t = line.split(); C[int(t[0])] = (Fraction(t[1]), t[2], t[3])
    return C

def coprime_ok(A, n):
    return (len(set(A)) == len(A) and all(1 <= a < n for a in A) and
            all(math.gcd(A[i], A[j]) == 1 for i in range(len(A)) for j in range(i + 1, len(A))))

if __name__ == '__main__':
    red = '--red' in sys.argv; nums = [int(t) for t in sys.argv[2:] if not t.startswith('--')]
    C = claimed(sys.argv[1]); P = sieve(5000); bad = 0
    for n0, n1 in zip(nums[0::2], nums[1::2]):
        for n in range(n0, n1 + 1):
            M, A = solve(n, red)
            val = sum((Fraction(1, n - a) for a in A), Fraction(0))
            ok_set = coprime_ok(A, n) and val == M
            Sp = sum((Fraction(1, p) for p in P if p < n), Fraction(0))
            E = '%.6f' % float(M - Sp)
            cM, cE, mark = C.get(n, (None, None, None))
            agree = (cM == M) and (cE == E)
            if not (agree and ok_set): bad += 1
            print('n=%d M=%s set_ok=%s table_M_equal=%s table_E_equal=%s E=%s |A|=%d%s' %
                  (n, M if len(str(M)) < 60 else '%.12f' % float(M), ok_set, cM == M, cE == E, E, len(A),
                   '' if agree else '  <-- DISAGREE (table M=%s E=%s)' % (cM, cE)))
            sys.stdout.flush()
    print('rows not agreeing or with bad set:', bad)
