"""Checker A for Erdős #1159 (Python 3 standard library; written for this repository).
For each plane in witnesses.json: rebuild the plane, check that it is a projective plane of order q, check that every
line meets the listed set S in at least 1 and at most C points, and check by the counting lemma that no set does this
with C - 1 (so the least cap of that plane is exactly C).
  Desarguesian planes PG(2,q): GF(q) = GF(p)[X]/(modulus) (the field axioms are checked from the tables), points are
  the nonzero triples scaled so that the last nonzero coordinate is 1, and the line [a,b,c] is {ax + by + cz = 0}.
  Other planes: the file lists each line as q+1 point numbers.
Counting lemma: if s points meet every line in 1..c points then s^2 - (c(q+1)+1)s + c(q^2+q+1) <= 0; for c = C - 1 the
checker verifies that this fails for every s = 0..q^2+q+1.
Exits non-zero on any failure. Usage: python3 check1159_a.py witnesses.json"""
import itertools
import json
import os
import sys


def field(p, h, mod):
    q = p ** h
    if h == 1:
        add = [[(a + b) % p for b in range(q)] for a in range(q)]
        mul = [[(a * b) % p for b in range(q)] for a in range(q)]
    else:
        dig = [[(x // p ** i) % p for i in range(h)] for x in range(q)]
        num = lambda d: sum(c * p ** i for i, c in enumerate(d))
        add = [[num([(u + v) % p for u, v in zip(dig[a], dig[b])]) for b in range(q)] for a in range(q)]
        mul = [[0] * q for _ in range(q)]
        for a in range(q):
            for b in range(q):
                r = [0] * (2 * h - 1)
                for i, u in enumerate(dig[a]):
                    for j, v in enumerate(dig[b]):
                        r[i + j] = (r[i + j] + u * v) % p
                for d in range(2 * h - 2, h - 1, -1):      # reduce by the monic modulus
                    c = r[d]
                    if c:
                        for k in range(h + 1):
                            r[d - h + k] = (r[d - h + k] - c * mod[k]) % p
                mul[a][b] = num(r[:h])
    R = range(q)
    assert all(add[a][b] == add[b][a] and mul[a][b] == mul[b][a] for a in R for b in R), 'not commutative'
    assert all(add[add[a][b]][c] == add[a][add[b][c]] and mul[mul[a][b]][c] == mul[a][mul[b][c]]
               and mul[a][add[b][c]] == add[mul[a][b]][mul[a][c]] for a in R for b in R for c in R), 'axiom fails'
    assert all(add[0][a] == a and mul[1][a] == a for a in R), 'identities'
    assert all(any(add[a][b] == 0 for b in R) for a in R), 'additive inverses'
    assert all(any(mul[a][b] == 1 for b in R) for a in R if a), 'not a field (the modulus is reducible)'
    return q, add, mul


def pg(p, h, mod):
    q, add, mul = field(p, h, mod)
    pts = [(x, y, 1) for x in range(q) for y in range(q)] + [(x, 1, 0) for x in range(q)] + [(1, 0, 0)]
    idx = {P: i for i, P in enumerate(pts)}
    lines = [[idx[P] for P in pts if add[add[mul[a][P[0]]][mul[b][P[1]]]][mul[c][P[2]]] == 0] for (a, b, c) in pts]
    return q, pts, idx, lines


def plane_ok(N, q, lines):
    if N != q * q + q + 1 or len(lines) != N or any(len(set(L)) != q + 1 or not set(L) <= set(range(N)) for L in lines):
        return False
    seen = set()
    for L in lines:
        for pr in itertools.combinations(sorted(L), 2):
            if pr in seen:
                return False
            seen.add(pr)
    return len(seen) == N * (N - 1) // 2


def counting_excludes(q, c):
    N = q * q + q + 1
    return all(s * s - (c * (q + 1) + 1) * s + c * N > 0 for s in range(N + 1))


data = json.load(open(sys.argv[1]))
base = os.path.dirname(os.path.abspath(sys.argv[1]))
fails = 0
for e in data:
    q, C = e['q'], e['C']
    if 'file' in e:
        lines = [[int(x) for x in l.split()] for l in open(os.path.join(base, '..', e['file'])) if l.strip()]
        N = len(lines)
        S = set(e['points'])
        valid_pts = len(S) == len(e['points']) and S <= set(range(N))
    else:
        try:
            q2, pts, idx, lines = pg(e['p'], e['h'], e['modulus'])
        except AssertionError as err:
            print('FAIL %-27s q=%-2d %s' % (e['plane'], q, err))
            fails += 1
            continue
        N = len(pts)
        assert q2 == q
        S = set()
        valid_pts = True
        for P in e['points']:
            if tuple(P) not in idx or idx[tuple(P)] in S:
                valid_pts = False
            else:
                S.add(idx[tuple(P)])
    pok = plane_ok(N, q, lines)
    loads = [len(S & set(L)) for L in lines]
    lo, hi = min(loads), max(loads)
    cnt = counting_excludes(q, C - 1)
    good = valid_pts and pok and lo >= 1 and hi <= C and cnt
    fails += not good
    print('%s %-27s q=%-2d |S|=%-2d loads %d..%d  plane=%s  cap %d impossible by counting=%s  => least cap %d' % (
        'PASS' if good else 'FAIL', e['plane'], q, len(S), lo, hi, pok, C - 1, cnt, C))
sys.exit(1 if fails else 0)
