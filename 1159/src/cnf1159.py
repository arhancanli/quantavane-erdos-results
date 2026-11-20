# CNF for "a point set meeting every line in 1..C points" in a plane given as a line list (Moorhouse format, or
# 'pg:p^h' / 'singer:p^h'): variable i+1 = point i in S; per line: one at-least-one clause and, for every
# (C+1)-subset of the line, a clause forbidding all of it. No symmetry breaking. DIMACS to stdout.
import sys, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
spec, C = sys.argv[1], int(sys.argv[2])
if spec.startswith('singer:'):
    from singer import singer
    p, h = map(int, spec[7:].split('^')) if '^' in spec[7:] else (int(spec[7:]), 1)
    q, N, D = singer(p, h); L = [[(x + j) % N for x in D] for j in range(N)]
else:
    L = [list(map(int, l.split())) for l in open(spec) if l.strip()]
n = max(max(l) for l in L) + 1
cl = [[x + 1 for x in l] for l in L]
for l in L:
    for sub in itertools.combinations(l, C + 1): cl.append([-(x + 1) for x in sub])
print('p cnf %d %d' % (n, len(cl)))
for c in cl: print(' '.join(map(str, c)) + ' 0')
