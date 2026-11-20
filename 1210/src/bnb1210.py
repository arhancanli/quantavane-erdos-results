# Program B for #1210 (exact): M(n) = max over pairwise coprime A in [1, n) of sum_{a in A} 1/(n-a).
# 1 is coprime to everything and is always taken. Exact integer weights w(a) = L/(n-a), L = lcm(1..n-1).
# Branch and bound over candidates a = n-1 down to 2; bound: chosen elements are pairwise coprime, hence have distinct
# largest prime factors P(a), so the remaining gain is at most sum over unused primes p of max{w(a): a remaining,
# compatible, P(a) = p}. Prints M(n) as an exact fraction, sum_{p<n} 1/p, the excess, and an optimal set.
import sys, math
sys.setrecursionlimit(100000)  # the DFS depth is at most the number of candidates (< n)
from fractions import Fraction
def factor_primes(a):
    ps, d = [], 2
    while d * d <= a:
        if a % d == 0:
            ps.append(d)
            while a % d == 0: a //= d
        d += 1
    if a > 1: ps.append(a)
    return ps
def solve(n):
    L = 1
    for k in range(1, n): L = L * k // math.gcd(L, k)
    cand = list(range(n - 1, 1, -1))
    pr = {a: frozenset(factor_primes(a)) for a in cand}
    w = {a: L // (n - a) for a in cand}
    P = {a: max(pr[a]) for a in cand}
    best = [0, []]
    def bound(rem, used):
        m = {}
        for a in rem:
            p = P[a]
            if w[a] > m.get(p, 0): m[p] = w[a]
        return sum(m.values())
    def dfs(i_rem, used, val, chosen):
        if val > best[0]: best[0], best[1] = val, list(chosen)
        if not i_rem: return
        if val + bound(i_rem, used) <= best[0]: return
        a = i_rem[0]; rest = i_rem[1:]
        # take a
        if not (pr[a] & used):
            nu = used | pr[a]
            dfs([b for b in rest if not (pr[b] & nu)], nu, val + w[a], chosen + [a])
        # skip a
        dfs(rest, used, val, chosen)
    dfs(cand, frozenset(), 0, [])
    M = Fraction(best[0], L) + Fraction(1, n - 1)  # plus the element 1
    return M, sorted(best[1] + [1])
if __name__ == '__main__':
    n0, n1 = int(sys.argv[1]), int(sys.argv[2])
    for n in range(n0, n1 + 1):
        M, A = solve(n)
        S = sum(Fraction(1, p) for p in range(2, n) if all(p % d for d in range(2, int(p ** .5) + 1)))
        print('n=%d M=%s (%.6f) sum1/p=%.6f excess=%.6f A=%s' % (n, M, float(M), float(S), float(M - S), A)); sys.stdout.flush()
