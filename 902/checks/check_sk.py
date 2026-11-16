"""Brute-force checker of Schutte's property S_k for a tournament given as an adjacency matrix file
(row i, column j is '1' iff i -> j). Checks it is a tournament, then every k-subset S (all of them, no symmetry)
for a vertex outside S beating all of S. Prints PASS or the first failing set. Usage: python3 check_sk.py file k"""
import sys, itertools
rows = [l.strip() for l in open(sys.argv[1]) if l.strip()]
k = int(sys.argv[2]); n = len(rows)
for i in range(n):
    if len(rows[i]) != n or rows[i][i] != '0': sys.exit(f'FAIL bad row {i}')
    for j in range(i + 1, n):
        if (rows[i][j] == '1') == (rows[j][i] == '1'): sys.exit(f'FAIL not a tournament at {i},{j}')
beats = [sum(1 << v for v in range(n) if rows[v][s] == '1') for s in range(n)]   # vertices v with v -> s
cnt = 0
for S in itertools.combinations(range(n), k):
    m = beats[S[0]]
    for s in S[1:]: m &= beats[s]
    cnt += 1
    if not m: print(f'FAIL n={n} k={k} undominated set {S}'); sys.exit(1)
print(f'PASS n={n} k={k}: all {cnt} {k}-sets dominated')
