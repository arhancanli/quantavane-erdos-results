# GF(p^h) arithmetic from a monic irreducible polynomial (found by search); elements are ints 0..q-1 (base-p digits).
def gf(p, h):
    q = p ** h
    def polymulmod(a, b, mod):
        # a, b, mod as coefficient lists (low to high), mod monic degree h
        r = [0] * (2 * h)
        for i, x in enumerate(a):
            for j, y in enumerate(b): r[i + j] = (r[i + j] + x * y) % p
        for d in range(2 * h - 1, h - 1, -1):
            c = r[d]
            if c:
                for k in range(h + 1): r[d - h + k] = (r[d - h + k] - c * mod[k]) % p
        return r[:h]
    def digits(x): return [(x // p ** i) % p for i in range(h)]
    def num(ds): return sum(d * p ** i for i, d in enumerate(ds))
    if h == 1:
        add = [[(a + b) % p for b in range(p)] for a in range(p)]; mul = [[(a * b) % p for b in range(p)] for a in range(p)]
        return q, add, mul
    import itertools
    for low in itertools.product(range(p), repeat=h):
        mod = list(low) + [1]
        # irreducible iff no root in GF(p^k) for... use: field iff every nonzero element has an inverse
        mul = [[num(polymulmod(digits(a), digits(b), mod)) for b in range(q)] for a in range(q)]
        if all(any(mul[a][b] == 1 for b in range(q)) for a in range(1, q)):
            add = [[num([(x + y) % p for x, y in zip(digits(a), digits(b))]) for b in range(q)] for a in range(q)]
            return q, add, mul
def pg2(p, h):
    q, add, mul = gf(p, h)
    pts = [(x, y, 1) for x in range(q) for y in range(q)] + [(x, 1, 0) for x in range(q)] + [(1, 0, 0)]
    lines = pts  # line [a,b,c] contains point (x,y,z) iff ax+by+cz = 0; lines indexed by normalized triples
    inc = []
    for (a, b, c) in lines:
        inc.append([i for i, (x, y, z) in enumerate(pts) if add[add[mul[a][x]][mul[b][y]]][mul[c][z]] == 0])
    return q, len(pts), inc
