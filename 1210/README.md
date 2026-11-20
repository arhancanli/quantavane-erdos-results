# Erdős Problem #1210: M(n) exactly for every 3 ≤ n ≤ 1794

Computed values for finitely many n; not a solution of the problem.

## The problem

As stated in [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
(`FormalConjectures/ErdosProblems/1210.lean`; [erdosproblems.com/1210](https://www.erdosproblems.com/1210)): let
A ⊆ [1, n) be a set of integers with (a, b) = 1 for all distinct a, b ∈ A. Is it true that
∑_{a∈A} 1/(n − a) ≤ ∑_{p<n} 1/p + O(1)?

Write M(n) for the maximum of ∑_{a∈A} 1/(n − a) over such A, and E(n) = M(n) − ∑_{p<n} 1/p. The question asks
whether E(n) is bounded above.

## Credits and what was known

- Eric Li, [arXiv:2606.17955](https://arxiv.org/abs/2606.17955) (2026), proved that ∑_{n≤N} M(n) = e^{−γ} N log log N
  + O(N), that M(n) ~ e^{−γ} log log n for almost all n, and that M(n) ≤ (2 + ε) log log n; it has no table of exact
  values. Erdős's sources are [Er77c] and [Er80], where he says the problem was not stated quite correctly at first
  (the formal-conjectures file states both forms).
- We found no table of M(n) (OEIS by the first numerators, GitHub, the plasma-ai/erdos record and the problem's page,
  searched 18 November 2026).

## What was computed

M(n) as a reduced fraction, E(n), and a maximising set, for every n from 3 to 1794 (`results/table.txt`). The largest
E(n) in each range:

    n             3-100       101-250   251-500   501-1000   1001-1500   1501-1794
    max E(n)      1 (3,4,6)   0.9695    0.9569    0.9577     0.9372      0.9314
    at n                      204       294       504        1044        1644

So E(n) < 1 for every n in this range except n = 3, 4, 6, where E(n) = 1; the largest values occur at n with many
small prime factors, and the smallest E(n) is about 0.19 (n = 1471). This is data: it neither proves nor refutes the
O(1) bound.

## Method

1 is coprime to everything and always belongs to a maximiser; for the rest, an exact branch and bound with integer
weights L/(n − a), L = lcm(1, …, n − 1), uses the fact that elements of a pairwise coprime set have distinct largest
prime factors, so the remaining gain is at most the sum, over primes p, of the largest weight with largest prime
factor p.

## How it was checked

- Two separately written programs: `src/bnb1210.py` (exact branch and bound, every n; it also ran to n = 2000, but
  rows above 1794 are not included because the independent checks stop there) and `src/ilp1210.py` (integer
  programme with HiGHS; its set, re-valued exactly, equals the table at every n ≤ 331, marked "A"). Full enumeration
  of every pairwise coprime set (`src/brute1210.py`) agrees for n ≤ 26.
- Referee: a separate AI session, given only the claim and the programs, wrote an exact dynamic programme over the
  primes up to √(n − 1) (`checks/dp1210_referee.py`: no branch and bound, no floating point) and reproduced M(n) and
  E(n) for every n = 3, …, 1794, and checked every printed maximiser. Verdict: correct with minor issues (robustness
  and a comment; no value changed).
- In this repository: `checks/check1210.py` re-checks every maximiser (pairwise coprime by factorisation, exact value
  equal to M(n), E(n)); the quick run also recomputes M(n) by the dynamic programme and the branch and bound for
  n ≤ 300. Red controls: a set with two elements sharing a prime, a value with its numerator increased by 1, and the dynamic programme
  with the prime 2 ignored are refused.

## Rerun

    sh 1210/checks/run.sh           # Python 3 only, under half a minute
    sh 1210/checks/run.sh --full    # the dynamic programme for n ≤ 1000 and every 50th n to 1794 (a few minutes)
    sh 1210/checks/run.sh --all     # the dynamic programme for every n ≤ 1794 (about half an hour)
