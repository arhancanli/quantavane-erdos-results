# Program 2 for exact min_n f(n,t): brute force over every n in [0, M_t), M_t = prod_{p<t} p^{e_p} (f is periodic
# mod M_t by the Plasma reduction, which is re-proved in PROOF notes), computing s_t(n+j) from the definition
# with FULL multiplicity by trial division (no truncation, no patterns). Independent of bnb461.c.
import sys
t = int(sys.argv[1])
ps = [p for p in range(2, t) if all(p % d for d in range(2, int(p ** .5) + 1))]
M = 1
for p in ps:
    q = 1
    while q < t: q *= p
    M *= q
def s(m):
    r = 1
    for p in ps:
        while m % p == 0: m //= p; r *= p
    return r
best = t + 1; arg = None
for n in range(M):
    f = len({s(n + j) for j in range(1, t + 1)})
    if f < best: best, arg = f, n
print('t=%d M_t=%d min_f=%d attained at n=%d' % (t, M, best, arg))
