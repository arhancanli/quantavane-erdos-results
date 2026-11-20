"""Checker for the Erdős #1210 table (Python 3 standard library; written for this repository, separately from the
programs in src/ and from checks/dp1210_referee.py).
For every row "n M(n) E(n) mark A": A is a set of distinct integers in [1, n); its elements are pairwise coprime
(tested by factoring each element and requiring that no prime divides two of them); sum_{a in A} 1/(n-a) equals M(n)
exactly (integer arithmetic over L = lcm(1, ..., n-1)); M(n) is in lowest terms; and E(n) is M(n) - sum_{p<n} 1/p
rounded to 6 decimals. The rows must be n = n_first, n_first + 1, ... with no gap.
This checks that each M(n) is attained; that it is the maximum is checked by the exhaustive programs.
Exits non-zero on any failure. Usage: python3 check1210.py table.txt"""
import sys
from fractions import Fraction
from math import gcd


def prime_factors(a):
    out, d = set(), 2
    while d * d <= a:
        while a % d == 0:
            out.add(d)
            a //= d
        d += 1
    if a > 1:
        out.add(a)
    return out


def is_prime(p):
    return p > 1 and all(p % d for d in range(2, int(p ** 0.5) + 1))


rows = []
for line in open(sys.argv[1]):
    t = line.split()
    if not t or t[0].startswith('#'):
        continue
    rows.append((int(t[0]), t[1], t[2], [int(x) for x in t[4].split(',')]))
errors = []
n0 = rows[0][0]
L = 1
for k in range(1, n0 - 1):
    L = L * k // gcd(L, k)
Sp = sum((Fraction(1, p) for p in range(2, n0 - 1) if is_prime(p)), Fraction(0))
for i, (n, Ms, Es, A) in enumerate(rows):
    if n != n0 + i:
        errors.append('row %d: n = %d, expected %d' % (i, n, n0 + i))
        break
    L = L * (n - 1) // gcd(L, n - 1)              # now L = lcm(1, ..., n-1)
    if is_prime(n - 1):
        Sp += Fraction(1, n - 1)                    # now Sp = sum of 1/p over primes p < n
    num, den = (int(x) for x in Ms.split('/')) if '/' in Ms else (int(Ms), 1)
    if gcd(num, den) != 1:
        errors.append('n=%d: M not in lowest terms' % n)
    if len(set(A)) != len(A) or any(not 1 <= a < n for a in A):
        errors.append('n=%d: elements repeated or outside [1, n)' % n)
        continue
    used = {}
    for a in A:
        for p in prime_factors(a):
            if p in used:
                errors.append('n=%d: %d and %d share the prime %d' % (n, used[p], a, p))
            used[p] = a
    total = sum(L // (n - a) for a in A)
    if total * den != num * L:
        errors.append('n=%d: the set sums to %s, not %s' % (n, Fraction(total, L), Ms))
    if '%.6f' % float(Fraction(num, den) - Sp) != Es:
        errors.append('n=%d: E(n) is %.6f, table says %s' % (n, float(Fraction(num, den) - Sp), Es))
for e in errors[:10]:
    print('FAIL', e)
if errors:
    sys.exit(1)
print('PASS %d rows (n = %d..%d): every set pairwise coprime in [1, n) with sum exactly M(n); E(n) correct'
      % (len(rows), rows[0][0], rows[-1][0]))
