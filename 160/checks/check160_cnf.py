"""Second checker for #160 colourings (separately written): builds the CNF of gen160.py (no symmetry breaking) for
the given N and k and evaluates every clause on the colouring; colours must lie in 0..k-1.
Usage: python3 check160_cnf.py file k"""
import sys, itertools
c = [int(t) for t in open(sys.argv[1]).read().split()]; k = int(sys.argv[2]); N = len(c)
if any(not 0 <= v < k for v in c): print(f'FAIL colour outside 0..{k-1}'); sys.exit(1)
x = lambda i, col: (i - 1) * k + col + 1
true = {x(i + 1, c[i]) for i in range(N)}
val = lambda l: (abs(l) in true) == (l > 0)
nbad = ncl = 0
for i in range(1, N + 1):
    for cl in [[x(i, col) for col in range(k)]] + [[-x(i, a), -x(i, b)] for a in range(k) for b in range(a + 1, k)]:
        ncl += 1; nbad += not any(val(l) for l in cl)
for a in range(1, N + 1):
    for d in range(1, (N - a) // 3 + 1):
        T = [a + t * d for t in range(4)]
        for P in itertools.combinations(range(k), 2):
            ncl += 1; nbad += not any(val(l) for l in [x(t, col) for t in T for col in range(k) if col not in P])
print(('PASS' if nbad == 0 else 'FAIL') + f' N={N} k={k}: {ncl} clauses, {nbad} violated'); sys.exit(1 if nbad else 0)
