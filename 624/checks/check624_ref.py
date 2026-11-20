# Referee checker for #624 (written without reusing the authors' code).
# Input: n, h and a table f as JSON {"i,j,k": value} (the authors' format) or as {mask: value}.
# Checks straight from the definition, for EVERY Y subset of [n] with |Y| >= h (not only |Y| = h):
#   {f(A) : A subset of Y, A in the table} = [n] = {0..n-1}.
# Sets absent from the table are free: since only listed sets are used, every total extension also passes.
# Also checks that keys are valid subsets of [n] (no duplicates after parsing) and every value lies in [n].
# Usage: referee_624_check.py n h table.json [--corrupt-test]
#   --corrupt-test: red control; tries single-entry corruptions until one is found that must FAIL, and also maps
#   every value n-1 to 0 (value n-1 then cannot appear), and reports the checker's verdict on both.
import sys, json

def parse(f, n):
    F = {}
    for k, v in f.items():
        if isinstance(k, str) and (k == '' or ',' in k or k.isdigit()) and not k.startswith('m'):
            el = [int(t) for t in k.split(',') if t != '']
            if len(set(el)) != len(el) or any(not 0 <= e < n for e in el): return None, 'bad key %r' % k
            m = 0
            for e in el: m |= 1 << e
        else:
            m = int(k[1:])
        if m in F: return None, 'duplicate set %r' % k
        if not (isinstance(v, int) and 0 <= v < n): return None, 'value out of range at %r: %r' % (k, v)
        F[m] = v
    return F, None

def check(F, n, h):
    full = (1 << n) - 1
    for Y in range(1 << n):
        if bin(Y).count('1') < h: continue
        img = 0; A = Y
        while True:
            if A in F: img |= 1 << F[A]
            if A == 0: break
            A = (A - 1) & Y
        if img != full:
            return False, 'Y=%s misses %s' % ([i for i in range(n) if Y >> i & 1], [x for x in range(n) if not img >> x & 1])
    return True, 'all %d sets Y with |Y| >= %d covered' % (sum(1 for Y in range(1 << n) if bin(Y).count('1') >= h), h)

if __name__ == '__main__':
    n, h = int(sys.argv[1]), int(sys.argv[2]); raw = json.load(open(sys.argv[3]))
    F, err = parse(raw, n)
    if F is None: print('FAIL', err); sys.exit(1)
    ok, msg = check(F, n, h)
    print('%s n=%d h=%d sets_in_table=%d max|A|=%d: %s' % ('PASS' if ok else 'FAIL', n, h, len(F),
          max(bin(m).count('1') for m in F), msg))
    if '--corrupt-test' in sys.argv:
        G = {m: (0 if v == n - 1 else v) for m, v in F.items()}
        print('  red (all values n-1 -> 0):', check(G, n, h))
        found = None
        for m in sorted(F):
            for x in range(n):
                if x == F[m]: continue
                G = dict(F); G[m] = x
                r = check(G, n, h)
                if not r[0]: found = (m, F[m], x, r[1]); break
            if found: break
        print('  red (single entry %s: %d -> %d):' % ([i for i in range(n) if found[0] >> i & 1], found[1], found[2]),
              'FAIL,', found[3]) if found else print('  red single entry: no failing single corruption found')
