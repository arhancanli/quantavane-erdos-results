# Erdős Problem #535: f_3(N) exactly for every N ≤ 64

Computed values for N ≤ 64; not a solution of the problem.

## The problem

As stated in [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
(`FormalConjectures/ErdosProblems/535.lean`; [erdosproblems.com/535](https://www.erdosproblems.com/535)): for r ≥ 3
let f_r(N) be the largest size of a subset of {1, …, N} in which no r elements have the same pairwise greatest common
divisor. Erdős proved f_3(N) > N^{c / log log N} for some c > 0 and conjectured that this is also the right upper
bound; the formal statement asks whether f_r(N) ≤ N^{c / log log N} for all large N, for every r ≥ 3.

## Credits and what was known

- Bounds: Erdős (1964), N^{c/log log N} < f_3(N) and f_r(N) ≤ N^{3/4+o(1)}; Abbott and Hanson (1970),
  f_r(N) ≤ N^{1/2+o(1)}; the link with the sunflower problem (Erdős 1973) and the sharper bounds now available through
  it are set out on [erdosproblems.com/535](https://www.erdosproblems.com/535), in its forum thread, and on the
  [plasma-ai/erdos](https://github.com/plasma-ai/erdos) page for the problem.
- We found no table of exact values (OEIS by description and by the first terms, GitHub, and the plasma-ai/erdos
  record, searched 18 November 2026; the only numeric OEIS match, A071860, agrees up to N = 23 and then differs).

## What was computed

f_3(N) for N = 1, …, 64, with an optimal set for each N (`results/table.txt`):

    N       1   2   3   4-7   8   9-15   16-17   18-26   27-31   32-44   45-48   49-53   54-64
    f_3(N)  1   2   2   3     4   5      6       7       8       9       10      11      12

This is only r = 3 and small N, and says nothing about the asymptotic question.

## Method

Every forbidden triple (three numbers with equal pairwise gcds) is listed, and the largest set containing none of
them is found by an exact solver; the structure lemma that three numbers have all pairwise gcds equal to d exactly
when they are d·a', d·b', d·c' with a', b', c' pairwise coprime gives a second, independent way to list the triples.

## How it was checked

- Two separately written exact programs: `src/ilp535.py` (forbidden triples from the definition, integer programme
  with HiGHS; N ≤ 46, then stopped) and `src/cpsat535.py` (triples from the structure lemma, CP-SAT; every N ≤ 64,
  all runs proved optimal). Original logs: `results/ilp_A_run.log`, `results/cpsat_B_run.log`.
- Referee: a separate AI session, given only the claim and the programs, confirmed every N = 1, …, 64 by two methods
  of its own: a SAT encoding (the claimed size satisfiable, one more refuted with a proof checked by drat-trim) and a
  solver-free branch and bound (`checks/referee_535_bnb.c`). Verdict: correct with minor issues (missing asserts in
  the solver scripts, since added; no value changed).
- In this repository: two set checkers (`checks/check535.py` from the definition, `checks/check535_b.py` from the
  structure lemma) and a plain exhaustive search (`checks/search535.py`, Python, no solver) that re-derives every
  value; red controls (a set with a forbidden triple, a table with three values lowered) are refused.

## Rerun

    sh 535/checks/run.sh            # Python 3 only, a few seconds
    sh 535/checks/run.sh --full     # also the referee's C branch and bound
