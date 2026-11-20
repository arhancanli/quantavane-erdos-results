"""Checker B for the Erdős #535 table (written separately from check535.py; Python 3 standard library).
It uses the structure lemma instead of the definition: three distinct numbers have all pairwise gcds equal to d iff
they are d*a', d*b', d*c' with a', b', c' pairwise coprime. For each row "N f set" it tests every triple of the set
this way (d = gcd of the triple, quotients pairwise coprime), checks the set is in {1..N} with f elements, and checks
that the f column is non-decreasing with steps of at most 1. Exits non-zero on any failure.
Usage: python3 check535_b.py table.txt"""
import sys


def g(a, b):
    while b:
        a, b = b, a % b
    return a


rows = []
for line in open(sys.argv[1]):
    line = line.strip()
    if not line or line[0] == '#':
        continue
    parts = line.split()
    rows.append((int(parts[0]), int(parts[1]), sorted(set(int(x) for x in parts[2].split(',')))))
errors = []
last = None
for N, f, S in rows:
    if len(S) != f or S[0] < 1 or S[-1] > N:
        errors.append('N=%d: size or range' % N)
    k = len(S)
    for i in range(k):
        for j in range(i + 1, k):
            for l in range(j + 1, k):
                x, y, z = S[i], S[j], S[l]
                d = g(g(x, y), z)
                a, b, c = x // d, y // d, z // d
                if g(a, b) == 1 and g(a, c) == 1 and g(b, c) == 1:
                    errors.append('N=%d: %d, %d, %d have equal pairwise gcds (= %d)' % (N, x, y, z, d))
    if last is not None and f - last not in (0, 1):
        errors.append('N=%d: f steps by %d' % (N, f - last))
    last = f
if [r[0] for r in rows] != list(range(1, len(rows) + 1)):
    errors.append('rows are not N = 1, 2, ...')
for e in errors[:10]:
    print('FAIL', e)
if errors:
    sys.exit(1)
print('PASS %d rows: no set contains a triple d*(a,b,c) with a, b, c pairwise coprime' % len(rows))
