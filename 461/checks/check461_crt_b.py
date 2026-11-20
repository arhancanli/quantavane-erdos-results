# Referee CRT check for Erdos #461 (independent of exact461.py).
# Input: t, a convention flag, then one residue per prime p < t.
#   conv "neg": tokens "p:r" mean position j has p-exponent a iff j = r mod p^a, i.e. n = -r mod p^{e_p}
#               (the convention printed by bnb461r.c);
#   conv "pos": tokens "p^e:x" mean n = x mod p^e (the convention printed by referee_min461.c).
# Rebuilds n by CRT with a hand-written extended Euclid, then computes s_t(n+j) for j = 1..t from the definition
# (product of p^v exactly dividing n+j over primes p < t, full multiplicity) and counts distinct values.
import sys

def egcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def is_prime(q):
    if q < 2:
        return False
    d = 2
    while d * d <= q:
        if q % d == 0:
            return False
        d += 1
    return True

def main():
    t = int(sys.argv[1]); conv = sys.argv[2]; toks = sys.argv[3:]
    primes = [q for q in range(2, t) if is_prime(q)]
    cong = {}
    for tok in toks:
        if conv == 'neg':
            p, r = map(int, tok.split(':'))
            e = 0; q = 1
            while q < t:
                q *= p; e += 1
            cong[p] = ((-r) % q, q)
        else:
            pe, x = tok.split(':'); p, e = map(int, pe.split('^')); q = p ** e
            assert q >= t and q // p < t, 'exponent is not the least with p^e >= t'
            cong[p] = (int(x) % q, q)
    assert sorted(cong) == primes, ('residues must cover exactly the primes < t', sorted(cong), primes)
    n, M = 0, 1
    for p in primes:
        x, q = cong[p]
        g, u, _ = egcd(M % q, q)
        assert g == 1
        k = ((x - n) * u) % q
        n, M = n + M * k, M * q
    for p in primes:
        x, q = cong[p]
        assert n % q == x
    assert 0 <= n < M
    def s(m):
        r = 1
        for p in primes:
            while m % p == 0:
                m //= p; r *= p
        return r
    vals = [s(n + j) for j in range(1, t + 1)]
    d = len(set(vals))
    hub = t // 2 + 1 if t >= 3 else 1
    print('t=%d n=%d (%d digits) distinct s_t(n+1..n+t) = %d   hub bound floor(t/2)+1 = %d' % (t, n, len(str(n)), d, hub))
    print('values:', vals)
    return d

if __name__ == '__main__':
    main()
