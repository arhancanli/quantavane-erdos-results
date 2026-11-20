# Program A for #1210 (separately written): ILP over x_a in {0,1}, a in [1, n-1]; for each prime p < n at most one
# chosen a divisible by p; maximise sum x_a/(n-a) (HiGHS, floats). The chosen set is re-valued EXACTLY (fractions)
# and checked to be pairwise coprime; the exact value is printed for comparison with program B.
import sys, math
from fractions import Fraction
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
def primes(x):
    s = bytearray([1]) * (x + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(x ** .5) + 1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(x + 1) if s[i]]
n0, n1 = int(sys.argv[1]), int(sys.argv[2])
for n in range(n0, n1 + 1):
    ps = primes(n - 1); m = n - 1
    data, ri, ci = [], [], []
    for i, p in enumerate(ps):
        for a in range(p, n, p): data.append(1); ri.append(i); ci.append(a - 1)
    Amat = coo_matrix((data, (ri, ci)), shape=(len(ps), m)).tocsr() if ps else None
    c = -np.array([1.0 / (n - a) for a in range(1, n)])
    cons = [LinearConstraint(Amat, -np.inf, 1)] if ps else []
    res = milp(c=c, constraints=cons, integrality=np.ones(m), bounds=Bounds(0, 1), options={'mip_rel_gap': 1e-12})
    A = [a + 1 for a in range(m) if res.x[a] > 0.5]
    assert all(math.gcd(a, b) == 1 for i, a in enumerate(A) for b in A[i+1:]), 'not pairwise coprime'
    M = sum(Fraction(1, n - a) for a in A)
    print('n=%d M=%s status=%d A=%s' % (n, M, res.status, A)); sys.stdout.flush()
