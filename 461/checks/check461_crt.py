# Exact check for #461 (separate from sa461.c): read "p:r" residues (r = -n mod p^{e_p}), build n by CRT,
# compute s_t(m) = product of all prime powers p^v || m with p < t (full multiplicity) for m = n+1..n+t
# by trial division, count distinct values and print the multiplicity profile.
import sys, collections
t = int(sys.argv[1]); pairs = [tuple(map(int, x.split(':'))) for x in sys.argv[2:]]
n, M = 0, 1
for p, r in pairs:
    q = 1
    while q < t: q *= p
    # want n = -r mod q
    target = (-r) % q
    # CRT combine n mod M with target mod q
    inv = pow(M, -1, q); k = ((target - n) * inv) % q; n, M = n + M * k, M * q
ps = [p for p, r in pairs]
assert all(all(p % d for d in range(2, int(p**.5)+1)) for p in ps) and sorted(ps) == [p for p in range(2, t) if all(p % d for d in range(2, int(p**.5)+1))]
def smooth(m):
    s = 1
    for p in ps:
        while m % p == 0: m //= p; s *= p
    return s
vals = [smooth(n + j) for j in range(1, t + 1)]
c = collections.Counter(vals)
print('t=%d n has %d digits; distinct=%d ratio=%.4f; values with mult>=3: %d; max mult %d (value %d)' % (
    t, len(str(n)), len(c), len(c)/t, sum(1 for v in c.values() if v >= 3), max(c.values()), c.most_common(1)[0][0]))
print('multiplicity histogram:', sorted(collections.Counter(c.values()).items()))
print('small repeated values:', sorted((v, k) for v, k in c.items() if k >= 2)[:40])
