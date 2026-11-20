# Checker B for #624 (separately written): reads a function table "A -> x" (JSON from a SAT model) and verifies by
# brute force that every Y with |Y| = h (hence every larger Y) has {f(A): A subset of Y} = [n]; sets missing from the
# table (|A| > h) are irrelevant. Prints PASS/FAIL.
import sys, json, itertools
n, h = int(sys.argv[1]), int(sys.argv[2]); f = json.load(open(sys.argv[3]))
F = {tuple(sorted(int(t) for t in k.split(',') if t != '')): v for k, v in f.items()}
ok = True
for Y in itertools.combinations(range(n), h):
    img = {F[S] for k in range(h + 1) for S in itertools.combinations(Y, k) if S in F}
    if img != set(range(n)): ok = False; print('FAIL at Y =', Y, 'missing', sorted(set(range(n)) - img)); break
print('PASS' if ok else 'FAIL', 'n=%d h=%d sets=%d' % (n, h, len(F)))
