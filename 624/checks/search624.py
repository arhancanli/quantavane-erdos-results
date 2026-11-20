"""Exhaustive search for Erdős #624 at small n (Python 3 standard library; written for this repository, separately
from the SAT encoders in src/; no symmetry breaking of any kind).
Decides whether some f: P([n]) -> [n] has {f(A) : A subset of Y} = [n] for every Y with |Y| >= h. Only |Y| = h and
|A| <= h matter (a larger Y contains an h-set; larger A lie in no h-set). Backtracking assigns f to the sets of size
<= h one by one (in order of size, then lexicographically) and rejects a partial f as soon as some h-set Y has all of
its subsets assigned but misses a value. Prints "n h SAT" (with the f found, checked again from the definition at the
end) or "n h UNSAT". Usage: python3 search624.py n h"""
import sys
from itertools import combinations

n, h = int(sys.argv[1]), int(sys.argv[2])
sets = [frozenset(c) for k in range(h + 1) for c in combinations(range(n), k)]
pos = {A: i for i, A in enumerate(sets)}
Ys = [frozenset(c) for c in combinations(range(n), h)]
subsets = {Y: [pos[frozenset(c)] for k in range(h + 1) for c in combinations(sorted(Y), k)] for Y in Ys}
# the h-sets whose last subset (in the order above) is sets[i]: check them when sets[i] gets its value
due = [[] for _ in sets]
for Y in Ys:
    due[max(subsets[Y])].append(Y)
f = [None] * len(sets)
full = set(range(n))


def rec(i):
    if i == len(sets):
        return True
    for v in range(n):
        f[i] = v
        if all({f[j] for j in subsets[Y]} == full for Y in due[i]) and rec(i + 1):
            return True
    f[i] = None
    return False


if rec(0):
    for Y in [frozenset(c) for k in range(h, n + 1) for c in combinations(range(n), k)]:
        img = {f[pos[A]] for k in range(min(h, len(Y)) + 1) for A in map(frozenset, combinations(sorted(Y), k))}
        assert img == full, Y
    print(n, h, 'SAT', {','.join(map(str, sorted(A))): f[pos[A]] for A in sets})
else:
    print(n, h, 'UNSAT')
