# Erdős Problem #624: H(n) for n = 2, …, 11

Computed values for n ≤ 11; not a solution of the problem.

## The problem

As stated in [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
(`FormalConjectures/ErdosProblems/624.lean`; [erdosproblems.com/624](https://www.erdosproblems.com/624)): let X be a
set of size n and let H(n) be the least m such that some function f from the subsets of X to X has
{f(A) : A ⊆ Y} = X for every Y ⊆ X with |Y| ≥ m. Prove that H(n) − log₂ n → ∞.

The function f here is arbitrary, as in the formal statement. Erdős and Hajnal's 1968 paper reportedly also requires
f(A) ∉ A; the values below are not values of that variant (with that constraint, H(n) is larger for n = 2, 3, 5 and 6).

## Credits and what was known

- Erdős and Hajnal (1968): log₂ n ≤ H(n) < log₂ n + (3 + o(1)) log₂ log₂ n. Alon: H(2^k) ≥ k + 1. The
  [plasma-ai/erdos](https://github.com/plasma-ai/erdos) page for the problem records a cube-counting proof of
  H(2^h) ≥ h + 1, hence H(n) > log₂ n for n ≥ 3.
- Small cases are reported to have been discussed in the problem's forum thread on erdosproblems.com (a comment of
  18 September 2026); we have not been able to compare our values with that comment, so they are offered as checked
  values, not as a priority claim.

## What was computed

    n            2      3      4      5      6      7      8      9      10     11
    H(n)         1      2      3      3      3      4      4      4      4      4
    H(n)−log₂n   0      0.415  1      0.678  0.415  1.193  1      0.830  0.678  0.541

Each upper bound is an explicit f (`results/witnesses/f_n<n>_h<H>.json`; sets of size larger than H(n) are free and
not listed). Each lower bound H(n) > H(n) − 1 comes from counting (2^{H−1} < n) for n = 2, 3, 5, 6, 9, 10, 11; from a
certificate of unsatisfiability for n = 4 and 7; and from H(7) ≤ H(8) for n = 8 (`results/table.txt`). n = 12 was not
decided.

## Method

A SAT encoding with one variable for each set A of size at most h and value x, a clause for every h-set Y and value x
saying that some subset of Y takes the value x, and at most one value per set; the values of a working f may be
renamed, so the encoding may fix f(∅) = 0 and require each value v ≥ 1 to appear first after v − 1 (both are sound by
this renaming argument, which the referee checked). Satisfying assignments give the tables f; unsatisfiable instances
give the lower bounds, with checked proofs.

## How it was checked

- Upper bounds: every table f is checked from the definition by two separately written checkers,
  `checks/check624.py` (every Y with |Y| = h) and the referee's `checks/check624_ref.py` (every Y with |Y| ≥ h).
- Lower bounds: the CNFs of `src/enc624.py` for (n, h) = (4, 2) and (7, 3) are stored in `results/certificates/`
  with LRAT proofs (CaDiCaL), which pass two separately written LRAT checkers (`checks/lrat_check.py`, Python, and
  `checks/lratcheck.c`, C, both at the top of the repository); the CNFs were first refuted with DRAT proofs checked by
  drat-trim. A second encoder written separately (`src/enc624b.py`: bitmasks, sequential-counter at-most-one, no
  precedence) gave the same answers where it was run. `checks/search624.py` (plain backtracking, no SAT and no symmetry
  breaking) confirms H(n) for n ≤ 4 and the lower bounds for n ≤ 6 on its own.
- Referee: a separate AI session, given only the claim, the lemmas and the programs, wrote its own encoding (all 2^n
  sets, coverage for every Y with |Y| ≥ h, and either no symmetry breaking or its own precedence order) and confirmed
  all ten values, with drat-trim-checked proofs for (n, h) = (2,0), (3,1), (4,2), (5,2), (6,2), (7,3), (8,3). Verdict:
  correct with minor issues (presentation: label the table "f arbitrary"; no value changed).
- Red controls: two corrupted tables, the n = 7 table used one level too low, and a truncated proof are refused.

## Rerun

    sh 624/checks/run.sh            # Python 3 only, a few seconds
    sh 624/checks/run.sh --full     # also the C LRAT checker
