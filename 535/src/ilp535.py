# Program A for #535: f_r(N) = max |A|, A in {1..N}, with no r-subset whose pairwise gcds are all equal.
# Forbidden r-sets enumerated directly from the definition (all r-subsets with constant pairwise gcd);
# exact ILP (HiGHS via scipy.optimize.milp): maximise sum x_a subject to sum_{a in S} x_a <= r-1 per forbidden S.
import sys, itertools, math, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
r = int(sys.argv[1]); Nmax = int(sys.argv[2])
for N in range(1, Nmax + 1):
    t0 = time.time()
    rows = []
    for S in itertools.combinations(range(1, N + 1), r):
        g = math.gcd(S[0], S[1])
        if all(math.gcd(a, b) == g for a, b in itertools.combinations(S, 2)):
            rows.append(S)
    if not rows:
        print('N=%d f=%d forbidden=0 set=all' % (N, N)); continue
    data, ri, ci = [], [], []
    for i, S in enumerate(rows):
        for a in S: data.append(1); ri.append(i); ci.append(a - 1)
    Amat = coo_matrix((data, (ri, ci)), shape=(len(rows), N)).tocsr()
    res = milp(c=-np.ones(N), constraints=[LinearConstraint(Amat, -np.inf, r - 1)], integrality=np.ones(N), bounds=Bounds(0, 1))
    if res.status != 0: print('N=%d SOLVER STATUS %d (not optimal) - stop' % (N, res.status)); sys.exit(1)
    x = np.round(res.x).astype(int); A = [a + 1 for a in range(N) if x[a]]
    for S in itertools.combinations(A, r):   # re-check the optimal set against the definition
        g = math.gcd(S[0], S[1]); assert not all(math.gcd(a, b) == g for a, b in itertools.combinations(S, 2)), S
    print('N=%d f=%d forbidden=%d status=%d time=%.1fs set=%s' % (N, len(A), len(rows), res.status, time.time() - t0, A)); sys.stdout.flush()
