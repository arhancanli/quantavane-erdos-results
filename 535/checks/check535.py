"""Checker A for the Erdős #535 table (Python 3 standard library), straight from the definition.
For every row "N f set": the set lies in {1, ..., N}, has f distinct elements, and no three of its elements have
gcd(a,b) = gcd(b,c) = gcd(a,c); also f(1) = 1 and f(N) - f(N-1) is 0 or 1. If a second file is given ("N f ..." per
line, e.g. the output of search535.py), its f must equal the table's at every N it lists.
Exits non-zero on any failure. Usage: python3 check535.py table.txt [other.txt]"""
import sys
from itertools import combinations
from math import gcd


def rows(path):
    out = {}
    for line in open(path):
        t = line.split()
        if not t or t[0].startswith('#'):
            continue
        out[int(t[0])] = (int(t[1]), [int(x) for x in t[2].split(',')] if len(t) > 2 and t[2] != '-' else [])
    return out


T = rows(sys.argv[1])
bad = 0
prev = 0
for N in sorted(T):
    f, A = T[N]
    msg = None
    if len(set(A)) != len(A) or len(A) != f:
        msg = 'set has %d distinct elements, f = %d' % (len(set(A)), f)
    elif any(not 1 <= a <= N for a in A):
        msg = 'element outside 1..N'
    else:
        for a, b, c in combinations(sorted(A), 3):
            if gcd(a, b) == gcd(b, c) == gcd(a, c):
                msg = 'forbidden triple %s' % ((a, b, c),)
                break
    if msg is None and not 0 <= f - prev <= 1:
        msg = 'f jumps from %d to %d' % (prev, f)
    if msg:
        print('FAIL N=%d: %s' % (N, msg)); bad += 1
    prev = f
if sorted(T) != list(range(1, max(T) + 1)):
    print('FAIL: rows are not N = 1..%d' % max(T)); bad += 1
if len(sys.argv) > 2:
    O = rows(sys.argv[2])
    for N in sorted(O):
        if N not in T or O[N][0] != T[N][0]:
            print('FAIL N=%d: other file says %d, table %s' % (N, O[N][0], T.get(N, ('none',))[0])); bad += 1
if bad:
    sys.exit(1)
print('PASS %d rows (N = 1..%d): every set valid and of size f(N)%s' % (len(T), max(T), '; other file agrees' if len(sys.argv) > 2 else ''))
