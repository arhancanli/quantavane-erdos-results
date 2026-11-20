"""Exhaustive search for Erdős #535 (Python 3 standard library; written for this repository, separately from the
programs in src/ and from checks/referee_535_bnb.c).
f_3(N) = the largest size of a set A in {1, ..., N} with no three elements whose three pairwise gcds are equal.
Branch and bound over x = N, N-1, ..., 1 (take x or not); taking x deletes from the candidates every c that would
complete a forbidden triple {a, x, c} with an element a already taken. The only bound is |taken| + |candidates|.
Forbidden triples come straight from the definition (all three gcds compared). Prints "N f set" for N = N0..N1.
Usage: python3 search535.py N0 N1"""
import sys
from math import gcd


def solve(N):
    forb = [[0] * (N + 1) for _ in range(N + 1)]   # forb[a][b] = bitmask of c with {a, b, c} forbidden
    for a in range(1, N + 1):
        for b in range(a + 1, N + 1):
            g = gcd(a, b); m = 0
            for c in range(1, N + 1):
                if c != a and c != b and gcd(a, c) == g and gcd(b, c) == g:
                    m |= 1 << c
            forb[a][b] = forb[b][a] = m
    best = [0, []]

    def rec(cand, chosen):
        if len(chosen) > best[0]:
            best[0], best[1] = len(chosen), list(chosen)
        if len(chosen) + bin(cand).count('1') <= best[0]:
            return
        x = cand.bit_length() - 1
        rest = cand & ~(1 << x)
        kill = 0
        for a in chosen:
            kill |= forb[a][x]
        chosen.append(x)
        rec(rest & ~kill, chosen)
        chosen.pop()
        rec(rest, chosen)

    rec(sum(1 << c for c in range(1, N + 1)), [])
    return best[0], sorted(best[1])


if __name__ == '__main__':
    for N in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        f, A = solve(N)
        print(N, f, ','.join(map(str, A)))
        sys.stdout.flush()
