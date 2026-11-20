# RED CONTROL (deliberately wrong): src/dfs461.py with the prime 2 left out; it must disagree with the table
# (t = 10, 16, 20 give 4, 5, 6 instead of 6, 9, 11).
# Program 2b for exact min_n f(n,t) (Python, written separately from bnb461.c): residues r mod p^{e_p} grouped by
# the exact tuple of p-adic factors they give positions 1..t; DFS over primes with exact integer partial values
# (tuples of products), no symmetry breaking; prune when #distinct partial values >= best.
import sys
t = int(sys.argv[1]); best = int(sys.argv[2]) + 1 if len(sys.argv) > 2 else t + 1
ps = [p for p in range(3, t) if all(p % d for d in range(2, int(p ** .5) + 1))]
opts = []
for p in ps:
    q = 1
    while q < t: q *= p
    seen = set()
    for r in range(q):
        fac = []
        for j in range(1, t + 1):
            x, pa = 1, p
            while pa <= q and (j - r) % pa == 0: x *= p; pa *= p
            fac.append(x)
        seen.add(tuple(fac))
    opts.append(sorted(seen))
nodes = 0
def dfs(i, vals):
    global best, nodes
    nodes += 1
    d = len(set(vals))
    if d >= best: return
    if i == len(ps): best = d; return
    for fac in opts[i]:
        nv = tuple(a * b for a, b in zip(vals, fac))
        if len(set(nv)) < best: dfs(i + 1, nv)
dfs(0, tuple([1] * t))
print('t=%d min_f=%d nodes=%d' % (t, best - 0, nodes))
