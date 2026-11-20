# Program A for #1159: least C such that a projective plane has a point set meeting every line in 1..C points.
# CP-SAT feasibility for C = 3 (expected infeasible for q >= 5) and C = 4; witness re-checked by direct incidence.
import sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gf import pg2
from hall9 import plane
from ortools.sat.python import cp_model
def solve(n, inc, C, tl):
    m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(n)]
    for L in inc: m.Add(sum(x[i] for i in L) >= 1); m.Add(sum(x[i] for i in L) <= C)
    s = cp_model.CpSolver(); s.parameters.num_workers = 1; s.parameters.max_time_in_seconds = tl
    st = s.Solve(m)
    return s.StatusName(st), ([i for i in range(n) if s.Value(x[i])] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
for spec in sys.argv[1:]:
    if spec.startswith('file:'):
        path = spec[5:]; L = [list(map(int, l.split())) for l in open(path) if l.strip()]
        n = len(L); q = len(L[0]) - 1; inc = L; tag = 'moorhouse_' + path.rsplit('/', 1)[-1].replace('.txt', '')
        import itertools as _it
        assert n == q * q + q + 1 and all(len(set(l)) == q + 1 and max(l) < n for l in L)
        _pairs = set()
        for l in L:
            for pr in _it.combinations(sorted(l), 2): assert pr not in _pairs; _pairs.add(pr)
        assert len(_pairs) == n * (n - 1) // 2
    elif spec in ('hall9', 'dual9'):
        q, n, inc = plane('hall' if spec == 'hall9' else 'dual'); tag = spec
    else:
        p, h = map(int, spec.split('^')) if '^' in spec else (int(spec), 1)
        q, n, inc = pg2(p, h); tag = 'pg2_%d' % (p ** h)
    assert all(len(L) == q + 1 for L in inc) and len(inc) == n == q * q + q + 1
    out = {'plane': tag, 'q': q}
    for C in ((2, 3, 4, 5, 6) if q < 5 else (4, 5, 6)):   # C <= 3 impossible for q >= 5 (counting lemma, PROOF.md)
        st, S = solve(n, inc, C, 600)
        out[C] = st
        if S is not None:
            loads = [sum(1 for i in L if i in set(S)) for L in inc]
            assert min(loads) >= 1 and max(loads) <= C
            out['witness_C%d' % C] = S; out['size'] = len(S)
            break
    print(json.dumps({k: v for k, v in out.items() if not str(k).startswith('witness')}), flush=True)
    json.dump(out, open('results/%s_cap.json' % tag, 'w'))
