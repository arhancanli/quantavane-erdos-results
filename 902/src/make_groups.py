# Multiplication tables for groups G = Z_p x| Q, Q = Z_q1 x Z_q2, acting on Z_p by x -> r^(c1*y1+c2*y2) x.
# Element (x, y1, y2) -> index x + p*(y1 + q1*y2); identity is index 0.
import sys
def table(p, q1, q2, r, c1, c2):
    els = [(x, y1, y2) for y2 in range(q2) for y1 in range(q1) for x in range(p)]
    idx = {e: i for i, e in enumerate(els)}
    def act(y1, y2, x): return (pow(r, c1 * y1 + c2 * y2, p) * x) % p
    def mul(a, b): return ((a[0] + act(a[1], a[2], b[0])) % p, (a[1] + b[1]) % q1, (a[2] + b[2]) % q2)
    n = len(els)
    return n, [[idx[mul(a, b)] for b in els] for a in els]
specs = {
 'Z7xZ7': (7, 7, 1, 1, 0, 0), 'Z11sZ5': (11, 5, 1, 3, 1, 0), 'Z19sZ3': (19, 3, 1, 7, 1, 0),
 'Z7sZ9': (7, 9, 1, 2, 1, 0), 'Z3xZ7sZ3': (7, 3, 3, 2, 1, 0), 'Z3xZ21': (7, 3, 3, 1, 0, 0),
 'Z19': (19, 1, 1, 1, 0, 0), 'Z7sZ3': (7, 3, 1, 2, 1, 0), 'Z17': (17, 1, 1, 1, 0, 0),
}
# Usage: python3 make_groups.py OUTDIR NAME [NAME ...]; NAME is a key of specs or Zc<n> for the cyclic group Z_n.
outdir = sys.argv[1]
for name in sys.argv[2:]:
    if name.startswith('Zc'):
        n = int(name[2:]); T = [[(a + g) % n for g in range(n)] for a in range(n)]
    else:
        n, T = table(*specs[name])
    with open(f'{outdir}/group_{name}.txt', 'w') as f:
        f.write(f'{n}\n'); [f.write(' '.join(map(str, row)) + '\n') for row in T]
    print(name, n)
