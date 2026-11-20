# Program B for #535 (separately written): f_3(N) by OR-tools CP-SAT. Forbidden triples generated structurally:
# gcd(a,b) = gcd(b,c) = gcd(a,c) = d  <=>  (a,b,c) = d*(a',b',c') with a',b',c' pairwise coprime (distinct).
# The optimal set is re-checked against ALL triples by brute force (math.gcd), independently of the generator.
import sys, math, itertools, time
from ortools.sat.python import cp_model
def triples(N):
    T = set()
    for d in range(1, N + 1):
        m = N // d
        for a in range(1, m + 1):
            for b in range(a + 1, m + 1):
                if math.gcd(a, b) != 1: continue
                for c in range(b + 1, m + 1):
                    if math.gcd(a, c) == 1 and math.gcd(b, c) == 1: T.add((d * a, d * b, d * c))
    return T
def bad(A):
    for x, y, z in itertools.combinations(sorted(A), 3):
        g = math.gcd(x, y)
        if math.gcd(y, z) == g and math.gcd(x, z) == g: return (x, y, z)
    return None
N0, N1 = int(sys.argv[1]), int(sys.argv[2])
for N in range(N0, N1 + 1):
    t0 = time.time(); T = triples(N)
    mdl = cp_model.CpModel(); x = {a: mdl.NewBoolVar('x%d' % a) for a in range(1, N + 1)}
    for (a, b, c) in T: mdl.AddBoolOr([x[a].Not(), x[b].Not(), x[c].Not()])
    mdl.Maximize(sum(x.values()))
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = 3600
    st = s.Solve(mdl)
    if st != cp_model.OPTIMAL: print('N=%d CP-SAT status %s (not optimal) - stop' % (N, s.StatusName(st))); sys.exit(1)
    A = [a for a in x if s.Value(x[a])]
    assert bad(A) is None
    print('N=%d f=%d optimal=%s triples=%d time=%.1fs set=%s' % (N, len(A), st == cp_model.OPTIMAL, len(T), time.time() - t0, A)); sys.stdout.flush()
