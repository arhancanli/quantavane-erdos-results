# Singer difference set for PG(2,q): GF(q^3) = GF(q)[x]/(x^3 - c2 x^2 - c1 x - c0) with x primitive; points of PG(2,q)
# are x^i, i mod N = q^2+q+1; the line {a + b x : a, b in GF(q)} gives D = {i : x^i has zero x^2-coefficient}.
# Lines of the plane are the translates D + j. Verified: D is a planar difference set (every nonzero residue mod N
# is a difference of exactly one ordered pair).
import sys, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gf import gf
def singer(p, h):
    q, add, mul = gf(p, h); N = q * q + q + 1; neg = [next(b for b in range(q) if add[a][b] == 0) for a in range(q)]
    def mulx(v, c):   # v = (v0, v1, v2) times x, with x^3 = c0 + c1 x + c2 x^2
        v0, v1, v2 = v
        return (mul[v2][c[0]], add[v0][mul[v2][c[1]]], add[v1][mul[v2][c[2]]])
    for c in itertools.product(range(q), repeat=3):
        if c[0] == 0: continue
        v = (1, 0, 0); order = None
        seen_scalar = None
        for i in range(1, q ** 3):
            v = mulx(v, c)
            if v[1] == 0 and v[2] == 0:   # x^i in GF(q): must first happen at i = N for x primitive in GF(q^3)/GF(q)...
                order = i; break
        if order != N: continue
        # check x has multiplicative order q^3 - 1 (primitive): x^N = scalar s with s of order q-1
        s = v[0]; t = s; k = 1
        while t != 1: t = mul[t][s]; k += 1
        if k != q - 1 and q > 2: continue
        D = []; v = (1, 0, 0)
        for i in range(N):
            if v[2] == 0: D.append(i)
            v = mulx(v, c)
        diffs = sorted((a - b) % N for a in D for b in D if a != b)
        if len(D) == q + 1 and diffs == list(range(1, N)): return q, N, D
    raise ValueError('no primitive cubic found')
if __name__ == '__main__':
    for spec in sys.argv[1:]:
        p, h = map(int, spec.split('^')) if '^' in spec else (int(spec), 1)
        q, N, D = singer(p, h); print('q=%d N=%d |D|=%d D=%s' % (q, N, len(D), D[:8]))
