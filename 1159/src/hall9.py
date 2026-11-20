# Nearfield (Hall) plane of order 9 and its dual. GF(9) from gf.py; Dickson nearfield product a o b = a*b if b is a
# nonzero square, a^3 * b otherwise (b != 0); 0 o b = a o 0 = 0. Translation plane: affine points (x,y); lines
# y = x o m + c (m, c in N), x = c; points at infinity (m) and (inf); line at infinity. Axioms verified by program.
import sys, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gf import gf
def plane(kind='hall'):
    q, add, mul = gf(3, 2)
    sq = {mul[a][a] for a in range(1, q)}
    def cube(a): return mul[mul[a][a]][a]
    def nmul(a, b):
        if a == 0 or b == 0: return 0
        return mul[a][b] if b in sq else mul[cube(a)][b]
    pts = [('a', x, y) for x in range(q) for y in range(q)] + [('m', m) for m in range(q)] + [('inf',)]
    P = {p: i for i, p in enumerate(pts)}
    lines = []
    for m in range(q):
        for c in range(q):
            lines.append([P[('a', x, add[nmul(x, m)][c])] for x in range(q)] + [P[('m', m)]])
    for c in range(q): lines.append([P[('a', c, y)] for y in range(q)] + [P[('inf',)]])
    lines.append([P[('m', m)] for m in range(q)] + [P[('inf',)]])
    n = len(pts)
    # verify: every line has q+1 points, every pair of points on exactly one line, n = q^2+q+1
    assert n == q * q + q + 1 and len(lines) == n and all(len(set(L)) == q + 1 for L in lines)
    cnt = {}
    for L in lines:
        for a, b in itertools.combinations(sorted(L), 2): cnt[(a, b)] = cnt.get((a, b), 0) + 1
    assert len(cnt) == n * (n - 1) // 2 and set(cnt.values()) == {1}
    if kind == 'dual':
        inc = [[j for j, L in enumerate(lines) if i in L] for i in range(n)]
        return q, n, inc
    return q, n, lines
if __name__ == '__main__':
    for k in ('hall', 'dual'):
        q, n, inc = plane(k); print(k, 'order', q, 'points', n, 'axioms OK')
