# Encoder B for #624 (written separately from enc624.py): sets as bitmasks; variable for (mask, x);
# at-most-one per mask by a sequential counter (Sinz); coverage: for every h-subset Y (bitmask) and value x,
# some submask A of Y with f(A) = x. Only symmetry used: f(emptyset) = 0 (rename values). DIMACS to stdout.
import sys
n, h = int(sys.argv[1]), int(sys.argv[2])
masks = [m for m in range(1 << n) if bin(m).count('1') <= h]
var = {}
def v(m, x):
    if (m, x) not in var: var[(m, x)] = len(var) + 1
    return var[(m, x)]
for m in masks:
    for x in range(n): v(m, x)
clauses = []; nv = len(var)
for m in masks:   # sequential counter AMO over v(m,0..n-1)
    s = []
    for i in range(n - 1): nv += 1; s.append(nv)
    xs = [v(m, x) for x in range(n)]
    for i in range(n - 1):
        clauses.append([-xs[i], s[i]])
        if i > 0: clauses.append([-s[i - 1], s[i]]); clauses.append([-xs[i], -s[i - 1]])
    clauses.append([-xs[n - 1], -s[n - 2]] if n > 1 else [])
for Y in masks:
    if bin(Y).count('1') != h: continue
    subs = []; A = Y
    while True:
        subs.append(A)
        if A == 0: break
        A = (A - 1) & Y
    for x in range(n): clauses.append([v(A, x) for A in subs])
clauses.append([v(0, 0)])
clauses = [c for c in clauses if c]
print('p cnf %d %d' % (nv, len(clauses)))
for c in clauses: print(' '.join(map(str, c)) + ' 0')
