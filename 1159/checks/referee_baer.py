"""Referee (separate session, own code): find a Baer subplane (a subplane of order 3, 13 points) in each plane of order 9, as an
independent route to a cap-4 set (a Baer subplane of a plane of order 9 meets every line in 1 or 4
points), and check that route directly on the incidence.
Usage: python3 -I referee_baer.py planes/   (PG(2,9) is built from the referee's own field). Exits non-zero unless
all four planes have one.
"""
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from referee_rplane import Field, PG2, verify_plane, read_moorhouse, loads  # noqa


def tables(lines, N):
    join = [[-1] * N for _ in range(N)]
    for li, L in enumerate(lines):
        for a in L:
            for b in L:
                if a != b:
                    join[a][b] = li
    meet = [[-1] * N for _ in range(N)]
    sets = [set(L) for L in lines]
    for i in range(N):
        for j in range(N):
            if i != j:
                meet[i][j] = next(iter(sets[i] & sets[j]))
    return join, meet


def closure(quad, lines, join, meet):
    P = set(quad)
    while True:
        Ls = {join[a][b] for a in P for b in P if a != b}
        newP = {meet[l][m] for l in Ls for m in Ls if l != m} | P
        if newP == P:
            return P, Ls
        P = newP
        if len(P) > 13:
            return P, Ls


def find_baer(lines, n=9):
    N = n * n + n + 1
    join, meet = tables(lines, N)
    tried = 0
    for b, c, d in itertools.combinations(range(1, N), 3):
        a = 0
        if len({join[a][b], join[a][c], join[b][c]}) < 3:
            continue
        if d in lines[join[a][b]] or d in lines[join[a][c]] or d in lines[join[b][c]]:
            continue
        tried += 1
        P, Ls = closure((a, b, c, d), lines, join, meet)
        if len(P) == 13:
            return sorted(P), tried
    return None, tried


def main():
    mdir = sys.argv[1]
    bad = 0
    F = Field(9)
    F.verify_axioms()
    planes = [("PG(2,9) (referee field)", PG2(F).lines)]
    for name in ("hall9", "dhall9", "hughes9"):
        planes.append((name + " (Moorhouse file)", read_moorhouse(os.path.join(mdir, name + ".txt"))))
    for name, lines in planes:
        verify_plane(lines, 9)
        B, tried = find_baer(lines)
        if B is None:
            print("FAIL %-26s no Baer subplane among %d quadrangles through point 0" % (name, tried))
            bad += 1
            continue
        L = loads(lines, B)
        hist = {k: L.count(k) for k in sorted(set(L))}
        good = set(L) <= {1, 4}
        bad += not good
        print("%s %-26s Baer subplane after %d quadrangles: %s; line loads %s -> cap-4 set: %s"
              % ("ok  " if good else "FAIL", name, tried, B, hist, good))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
