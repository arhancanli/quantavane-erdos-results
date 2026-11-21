"""Referee's own finite-field and projective-plane code for Erdos #1159 (written 20 Nov 2026 by a separate
session, without reading the lab's code). Python 3, standard library only.

Field GF(p^h): elements are integers 0..q-1; the base-p digits of an integer, least significant
first, are the coefficients of 1, t, t^2, ... of a polynomial in t, reduced modulo a monic
irreducible polynomial chosen here (coefficients listed constant term first).
"""
import itertools

# The referee's own choice of defining polynomials (constant term first, monic), made before reading
# the lab's code. Under the lab's convention (modulus listed constant term first) the GF(8) and GF(16)
# choices turned out to equal the lab's, so the witness check is also run with ALT_MODULI below.
REF_MODULI = {
    4: (2, [1, 1, 1]),        # t^2 + t + 1 (the only irreducible quadratic over GF(2))
    8: (2, [1, 0, 1, 1]),     # t^3 + t^2 + 1
    9: (3, [2, 1, 1]),        # t^2 + t + 2
    16: (2, [1, 0, 0, 1, 1]),  # t^4 + t^3 + 1
}
ALT_MODULI = {
    8: (2, [1, 1, 0, 1]),     # t^3 + t + 1
    9: (3, [1, 0, 1]),        # t^2 + 1
    16: (2, [1, 1, 0, 0, 1]),  # t^4 + t + 1
}


def digits(n, p, h):
    out = []
    for _ in range(h):
        out.append(n % p)
        n //= p
    return out


def undigits(ds, p):
    n = 0
    for c in reversed(ds):
        n = n * p + c
    return n


def poly_mulmod(a, b, mod, p):
    """a, b: coefficient lists (constant first) of length h; mod: monic, length h+1."""
    h = len(mod) - 1
    prod = [0] * (2 * h - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                prod[i + j] = (prod[i + j] + x * y) % p
    for d in range(len(prod) - 1, h - 1, -1):
        c = prod[d]
        if c:
            # subtract c * t^(d-h) * mod
            for k in range(h + 1):
                prod[d - h + k] = (prod[d - h + k] - c * mod[k]) % p
    return prod[:h]


class Field:
    def __init__(self, q):
        self.q = q
        if q in REF_MODULI:
            p, mod = REF_MODULI[q]
        else:
            p, mod = q, None
            assert all(q % d for d in range(2, q)), "q must be prime or listed"
        self.p = p
        self.mod = mod
        h = 1 if mod is None else len(mod) - 1
        self.h = h
        assert p ** h == q
        self.add = [[0] * q for _ in range(q)]
        self.mul = [[0] * q for _ in range(q)]
        for a in range(q):
            da = digits(a, p, h)
            for b in range(q):
                db = digits(b, p, h)
                self.add[a][b] = undigits([(x + y) % p for x, y in zip(da, db)], p)
                if mod is None:
                    self.mul[a][b] = (a * b) % p
                else:
                    self.mul[a][b] = undigits(poly_mulmod(da, db, mod, p), p)
        self.neg = [next(b for b in range(q) if self.add[a][b] == 0) for a in range(q)]
        self.inv = [None] + [next((b for b in range(q) if self.mul[a][b] == 1), None)
                             for a in range(1, q)]

    def verify_axioms(self):
        q, A, M = self.q, self.add, self.mul
        R = range(q)
        for a in R:
            assert A[a][0] == a and M[a][1] == a and M[a][0] == 0
            for b in R:
                assert A[a][b] == A[b][a] and M[a][b] == M[b][a]
        for a, b, c in itertools.product(R, R, R):
            assert A[A[a][b]][c] == A[a][A[b][c]]
            assert M[M[a][b]][c] == M[a][M[b][c]]
            assert M[a][A[b][c]] == A[M[a][b]][M[a][c]]
        assert all(self.inv[a] is not None for a in range(1, q)), "not a field (modulus reducible)"
        return True

    def eval_poly(self, coeffs_const_first, x):
        """Evaluate a polynomial with coefficients in the prime field (ints < p) at field element x."""
        acc = 0
        for c in reversed(coeffs_const_first):
            acc = self.add[self.mul[acc][x]][c]  # c < p is the prime-field element c
        return acc


class PG2:
    """PG(2,q) over a Field: points and lines are normalised triples (first nonzero entry 1)."""

    def __init__(self, F):
        self.F = F
        q = F.q
        pts = []
        for v in itertools.product(range(q), repeat=3):
            if any(v):
                first = next(x for x in v if x)
                if first == 1:
                    pts.append(v)
        self.points = pts
        self.index = {v: i for i, v in enumerate(pts)}
        A, M = F.add, F.mul
        lines = []
        for u in pts:  # line coordinates use the same normalised triples
            lines.append([i for i, v in enumerate(pts)
                          if A[A[M[u[0]][v[0]]][M[u[1]][v[1]]]][M[u[2]][v[2]]] == 0])
        self.lines = lines

    def normalise(self, v):
        F = self.F
        first = next(x for x in v if x)
        s = F.inv[first]
        return tuple(F.mul[s][x] for x in v)


def verify_plane(lines, n_order):
    """Projective plane of order n: n^2+n+1 points and lines, n+1 points per line,
    every pair of distinct points on exactly one line (checked by counting all pairs)."""
    N = n_order * n_order + n_order + 1
    assert len(lines) == N, (len(lines), N)
    pts = sorted(set(itertools.chain.from_iterable(lines)))
    assert pts == list(range(N)), "points are not 0..N-1"
    assert all(len(set(L)) == n_order + 1 == len(L) for L in lines)
    assert len(set(tuple(sorted(L)) for L in lines)) == N, "repeated line"
    seen = {}
    for li, L in enumerate(lines):
        for a, b in itertools.combinations(sorted(L), 2):
            assert (a, b) not in seen, "pair on two lines"
            seen[(a, b)] = li
    assert len(seen) == N * (N - 1) // 2, "some pair on no line"
    return True


def read_moorhouse(path):
    lines = []
    with open(path) as fh:
        for row in fh:
            row = row.strip()
            if row:
                lines.append([int(x) for x in row.split()])
    return lines


def loads(lines, S):
    S = set(S)
    return [sum(1 for x in L if x in S) for L in lines]


def counting_bound_ok(s, q, C):
    return s * s - (C * (q + 1) + 1) * s + C * (q * q + q + 1) <= 0
