# Encoder A for #624: is there f: P([n]) -> [n] with {f(A): A subset of Y} = [n] for every Y with |Y| >= h?
# Only sets of size <= h matter (every larger Y contains an h-subset). Variables v(A,x), |A| <= h.
# Clauses: for each A, at most one x (pairwise); for each h-set Y and each x, OR_{A subset Y} v(A,x).
# Optional certified symmetry breaking "--fix0": f(emptyset) = 0 (values may be renamed by any permutation of [n],
# which preserves the property; so if any f exists, one with f(empty) = 0 exists).
# Writes DIMACS to stdout; variable map to the file given as 4th argument.
import sys, itertools, json
n, h = int(sys.argv[1]), int(sys.argv[2]); fix0 = '--fix0' in sys.argv
sets = [frozenset(c) for k in range(h + 1) for c in itertools.combinations(range(n), k)]
idx = {}
for A in sets:
    for x in range(n): idx[(A, x)] = len(idx) + 1
cl = []
for A in sets:
    for x, y in itertools.combinations(range(n), 2): cl.append([-idx[(A, x)], -idx[(A, y)]])
for Y in itertools.combinations(range(n), h):
    subs = [frozenset(c) for k in range(h + 1) for c in itertools.combinations(Y, k)]
    for x in range(n): cl.append([idx[(A, x)] for A in subs])
if fix0: cl.append([idx[(frozenset(), 0)]])
if '--prec' in sys.argv:
    # value precedence (certified by renaming values in order of first appearance along the fixed order `sets`):
    # value v >= 1 may be taken by sets[k] only if value v-1 is taken by some sets[j], j < k.
    # Linear encoding: u(k,v) <-> OR_{j<=k} v(sets[j], v), with fresh variables.
    nxt = len(idx) + 1; U = {}
    for k in range(len(sets)):
        for v in range(n): U[(k, v)] = nxt; nxt += 1
    for k, A in enumerate(sets):
        for v in range(n):
            cl.append([-idx[(A, v)], U[(k, v)]])
            if k > 0:
                cl.append([-U[(k - 1, v)], U[(k, v)]])
                cl.append([-U[(k, v)], U[(k - 1, v)], idx[(A, v)]])
            else:
                cl.append([-U[(k, v)], idx[(A, v)]])
            if v >= 1:
                cl.append([-idx[(A, v)]] + ([U[(k - 1, v - 1)]] if k > 0 else []))
    nvars = nxt - 1
else:
    nvars = len(idx)
print('p cnf %d %d' % (nvars, len(cl)))
for c in cl: print(' '.join(map(str, c)) + ' 0')
if len(sys.argv) > 3 and not sys.argv[3].startswith('--'):
    json.dump({'%s|%d' % (','.join(map(str, sorted(A))), x): v for (A, x), v in idx.items()}, open(sys.argv[3], 'w'))
