"""Invariants of the group tables used for #902: order, abelian or not, number of elements of each order,
centre size; verifies identity, inverses and associativity independently of the C programs."""
import sys, collections
for path in sys.argv[1:]:
    L = open(path).read().split('\n'); n = int(L[0]); M = [list(map(int, L[1 + a].split())) for a in range(n)]
    assert all(M[0][a] == a and M[a][0] == a for a in range(n))
    assert all(any(M[a][b] == 0 for b in range(n)) for a in range(n))
    assert all(M[M[a][b]][c] == M[a][M[b][c]] for a in range(n) for b in range(n) for c in range(n))
    def order(a):
        k, x = 1, a
        while x != 0: x = M[x][a]; k += 1
        return k
    ab = all(M[a][b] == M[b][a] for a in range(n) for b in range(n))
    cen = sum(all(M[a][b] == M[b][a] for b in range(n)) for a in range(n))
    oc = sorted(collections.Counter(order(a) for a in range(n)).items())
    print(path.split('group_')[-1][:-4], n, 'abelian' if ab else 'nonabelian', 'centre', cen, 'orders', oc)
