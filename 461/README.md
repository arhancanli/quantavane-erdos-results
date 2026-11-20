# Erdős Problem #461: the exact minimum of f(n,t) over n, for every t ≤ 54 and even t ≤ 64

Computed values for finitely many t; not a solution of the problem.

## The problem

As stated in [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
(`FormalConjectures/ErdosProblems/461.lean`; [erdosproblems.com/461](https://www.erdosproblems.com/461)): let s_t(n) be
the t-smooth component of n, the product of all primes p < t dividing n, counted with multiplicity, and let f(n,t) be
the number of distinct values of s_t(m) for m in [n+1, n+t]. Is it true that f(n,t) ≫ t, uniformly for all t and n?
Erdős and Graham (1980) report that they can show f(n,t) ≫ t / log t.

## Credits and what was known

- The reduction used here is the one recorded on the [plasma-ai/erdos](https://github.com/plasma-ai/erdos) page for
  #461: with e_p the least exponent such that p^{e_p} ≥ t, f(n,t) depends only on n modulo M_t = ∏_{p<t} p^{e_p}, so
  min_n f(n,t) is a finite computation. That page gives the minima for t = 2 and 3 (1 and 2) and notes that no larger
  sweep was run.
- [OEIS A401328](https://oeis.org/A401328) (October 2026) tabulates f(n,k) itself, not its minimum over n.
- We found no table of min_n f(n,t) for larger t (OEIS, GitHub and the plasma-ai/erdos record, searched 18 November 2026).

## What was computed

m(t) = min over all n ≥ 0 of f(n,t), exactly, for t = 2, …, 54 and t = 56, 58, 60, 62, 64 (`results/table.txt`):

    t     2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33
    m(t)  1  2  3  3  4  4  5  5  6  6  7  7  8  8  9  9 10 10 11 11 12 12 13 13 14 14 15 15 16 16 17 17

    t    34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 56 58 60 62 64
    m(t) 18 18 19 19 20 20 21 21 22 22 22 23 23 23 24 24 25 25 26 27 27 28 28 29 30 31

So m(t) = ⌊t/2⌋ + 1 for 4 ≤ t ≤ 43 and for t = 45 and 53; m(t) = ⌊t/2⌋ for t = 44, 46–52, 54 and 56; and
m(t) = t/2 − 1 for t = 58, 60, 62 and 64. The value ⌊t/2⌋ + 1 is that of the "hub" choice of n, where n + h is
divisible by M_t for the middle position h; the hub is optimal up to t = 43 and is first beaten at t = 44. Every row
has an explicit n (`results/witnesses.txt`). The odd t from 55 to 63 (27, 28, 29, 30, 31) were found by one
exhaustive program only and are listed in the table but not counted here.

Larger t, upper bounds only: explicit n with f(n,160) = 75, f(n,640) = 268, f(n,1280) = 524 and
f(n,2560) = 1004 = 0.392 t (`results/witnesses_large.txt`, found by simulated annealing). So the minimum falls below
t/2. Whether it stays above a constant times t, which is the question, is not decided by any of this.

## Method

f(n,t) depends only on the residues of n modulo p^{e_p} (one residue per prime p < t), and only through the pattern
of p-adic valuations (capped at e_p) that each residue gives the positions 1, …, t; the programs search over these
patterns, prime by prime, and prune when the number of distinct partial values already reaches the best found, which
is valid because adding primes can only split classes.

## How it was checked

- Two separately written exhaustive programs: `src/bnb461.c` (C, exponent patterns, partition refinement, reflection
  symmetry broken; every listed t) and `src/dfs461.py` (Python, exact integer products, no symmetry breaking; t ≤ 25
  and even t ≤ 46). A brute force over every n mod M_t, from the definition, agrees for t ≤ 12.
- Referee: a separate AI session, given only the claimed table, the lemmas and the programs, wrote its own exhaustive
  program with a different characterisation of equality (`checks/referee_min461.c`: pairwise collision masks, no
  symmetry breaking), its own brute force (`checks/referee_brute461.c`, t ≤ 13) and its own CRT checker
  (`checks/check461_crt_b.py`), and reproduced every value, under several different prime orders. Verdict: correct
  with minor issues (documentation and an unsafe optional argument, since fixed; no value changed).
- Every witness is rebuilt by the Chinese remainder theorem and counted from the definition by two checkers
  (`checks/check461_crt.py`, `checks/check461_crt_b.py`).
- Red controls: a witness with one residue changed, the search with the prime 2 removed, an over-eager prune, and a
  variant with every cap set to 1 all disagree with the table.

## Rerun

    sh 461/checks/run.sh            # Python 3 only, under half a minute
    sh 461/checks/run.sh --full     # also compiles and reruns the C searches (about a minute)

`results/bnb_26_64.log` and `results/queue_exact.log` are the original logs of the exhaustive runs.
