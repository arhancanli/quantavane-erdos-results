"""Checker B for Erdős #1159 (Python 3 standard library; written separately from check1159_a.py).
Differences from checker A: field elements are coefficient vectors multiplied by schoolbook multiplication and reduction
(no tables), points are scaled so that the FIRST nonzero coordinate is 1, the lines of PG(2,q) are built as spans
{aP + bQ} of pairs of points (not from line coordinates), a plane read from a file is checked line against line (every
two lines meet in exactly one point, every point is on q+1 lines), and the lower bound uses the integer line-type
equations instead of the quadratic inequality: if every line meets S (|S| = s) in 1..c points and t_i lines meet it in
i points, then sum t_i = q^2+q+1, sum i t_i = s(q+1), sum i(i-1) t_i = s(s-1); the checker shows that for c = C - 1
these have no solution in nonnegative integers for any s. Exits non-zero on any failure.
Usage: python3 check1159_b.py witnesses.json"""
import json
import os
import sys


class GF:
    def __init__(self, p, h, mod):
        self.p, self.h, self.mod = p, h, (mod if mod else [0, 1])
        self.q = p ** h
        assert self.mod[-1] == 1 and len(self.mod) == h + 1

    def vec(self, x):
        return tuple((x // self.p ** i) % self.p for i in range(self.h))

    def add(self, u, v):
        return tuple((a + b) % self.p for a, b in zip(u, v))

    def mul(self, u, v):
        p, h = self.p, self.h
        r = [0] * (2 * h)
        for i in range(h):
            for j in range(h):
                r[i + j] += u[i] * v[j]
        for d in range(2 * h - 1, h - 1, -1):
            c = r[d] % p
            r[d] = 0
            for k in range(h):
                r[d - h + k] -= c * self.mod[k]
        return tuple(x % p for x in r[:h])

    def elements(self):
        return [self.vec(x) for x in range(self.q)]


def check_field(F):
    E = F.elements()
    one = F.vec(1)
    for a in E:
        if any(a) and not any(F.mul(a, b) == one for b in E):
            return False                      # a nonzero element without inverse: the modulus is reducible
    return True


def normalise(F, v):
    E = F.elements()
    first = next(x for x in v if any(x))
    inv = next(b for b in E if F.mul(first, b) == F.vec(1))
    return tuple(F.mul(inv, x) for x in v)


def pg_lines(F):
    E = F.elements()
    zero = F.vec(0)
    pts = sorted({normalise(F, (a, b, c)) for a in E for b in E for c in E if (a, b, c) != (zero, zero, zero)})
    covered, lines = set(), []
    for i, P in enumerate(pts):
        for Q in pts[i + 1:]:
            if (P, Q) in covered:
                continue
            L = set()
            for a in E:
                for b in E:
                    if a != zero or b != zero:
                        L.add(normalise(F, tuple(F.add(F.mul(a, x), F.mul(b, y)) for x, y in zip(P, Q))))
            for X in L:
                for Y in L:
                    covered.add((X, Y))
            lines.append(frozenset(L))
    return pts, lines


def no_line_types(q, c):
    N = q * q + q + 1
    for s in range(N + 1):
        A, B = s * (q + 1), s * (s - 1)
        rng = range(N + 1) if c >= 3 else [0]
        for t3 in rng:                         # c <= 3 here: t_3 free, then t_2 and t_1 are determined
            if 6 * t3 > B or (B - 6 * t3) % 2:
                continue
            t2 = (B - 6 * t3) // 2
            t1 = N - t2 - t3
            if t1 >= 0 and t1 + 2 * t2 + 3 * t3 == A:
                return False
    return True


data = json.load(open(sys.argv[1]))
base = os.path.dirname(os.path.abspath(sys.argv[1]))
bad = 0
for e in data:
    q, C = e['q'], e['C']
    N = q * q + q + 1
    if 'file' in e:
        lines = [frozenset(int(x) for x in l.split()) for l in open(os.path.join(base, '..', e['file'])) if l.strip()]
        S = set(e['points'])
        ok_pts = len(S) == len(e['points']) and all(0 <= x < N for x in S)
        ok_plane = (len(lines) == N and all(len(L) == q + 1 for L in lines)
                    and all(len(lines[i] & lines[j]) == 1 for i in range(N) for j in range(i + 1, N))
                    and all(sum(1 for L in lines if x in L) == q + 1 for x in range(N)))
        field_ok = True
    else:
        F = GF(e['p'], e['h'], e['modulus'])
        field_ok = check_field(F)
        if not field_ok:
            print('FAIL %-27s q=%-2d the modulus %s does not give a field' % (e['plane'], q, e['modulus']))
            bad += 1
            continue
        pts, lines = pg_lines(F)
        S = {normalise(F, tuple(F.vec(x) for x in P)) for P in e['points']}
        ok_pts = len(S) == len(e['points'])
        ok_plane = (len(pts) == N and len(lines) == N and all(len(L) == q + 1 for L in lines))
    loads = [len(S & L) for L in lines]
    lb = no_line_types(q, C - 1) if C - 1 <= 3 else False
    good = field_ok and ok_pts and ok_plane and min(loads) >= 1 and max(loads) <= C and lb
    bad += not good
    print('%s %-27s q=%-2d |S|=%-2d loads %d..%d  field=%s plane=%s  no line types for cap %d=%s' % (
        'PASS' if good else 'FAIL', e['plane'], q, len(S), min(loads), max(loads), field_ok, ok_plane, C - 1, lb))
sys.exit(1 if bad else 0)
