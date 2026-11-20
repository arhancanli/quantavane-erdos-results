# Erdős Problem #1159: the least cap of a blocking set in twelve small projective planes

Computed values for twelve particular planes; not a solution of the problem.

## The problem

As stated in [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
(`FormalConjectures/ErdosProblems/1159.lean`; [erdosproblems.com/1159](https://www.erdosproblems.com/1159)):
determine whether there exists a constant C > 1 such that every finite projective plane P has a set of points S with
1 ≤ |S ∩ ℓ| ≤ C for all lines ℓ.

For a plane Π, write c(Π) for the least C for which such a set exists in Π.

## Credits and what was known

- Erdős, Silverman and Stein (1983): for large orders q there is such a set with fewer than a·log q points on every
  line.
- The [plasma-ai/erdos](https://github.com/plasma-ai/erdos) record for #1159 gives the counting bound that rules out
  C = 3 in every plane of order q ≥ 5 (re-proved below), cap-4 sets in PG(2,5), PG(2,7) and PG(2,11), cap-5 and cap-6
  sets in some larger prime planes, and a construction with cap 6 in PG(2,2^h), h ≥ 2. So c = 4 for PG(2,5), PG(2,7)
  and PG(2,11) was already known there.
- Szőnyi's 1992 survey of blocking sets reports constant caps in Desarguesian planes of fixed characteristic: at most
  4 in PG(2,3^r) (Bruen and Fisher), at most p + 1 in PG(2,p^r) for odd p (Boros), and 5 or 6 in PG(2,2^r) (Illés,
  Szőnyi and Wettl). In particular a cap-4 set in PG(2,9) follows from Bruen and Fisher's result.
- The three non-Desarguesian planes of order 9 are read from G. Eric Moorhouse's list of projective planes
  (ericmoorhouse.org, `planes/hall9.txt`, `planes/dhall9.txt`, `planes/hughes9.txt`, used as data with credit to him).
  Lam, Kolesova and Thiel (1991) showed that there are exactly four planes of order 9.

## What was computed

    plane                         c(Π)    |S| of the set listed
    PG(2,2), PG(2,3), PG(2,4)       3     7, 6, 7
    PG(2,5), PG(2,7), PG(2,8)       4     10, 16, 18
    PG(2,9)                         4     22
    Hall plane of order 9           4     20
    dual Hall plane of order 9      4     20
    Hughes plane of order 9         4     20
    PG(2,11), PG(2,16)              4     21, 39

So all four planes of order 9 have least cap 4, and PG(2,8) and PG(2,16) have least cap 4, below the 5 or 6 of the
general constructions for PG(2,2^r). The sets are in `results/witnesses.json` (points of PG(2,q) as coordinate
triples over GF(q), with the field's defining polynomial; points of the other planes as numbers in Moorhouse's
files). PG(2,13) and PG(2,17) are not decided here, and nothing here bears on large orders.

## Method

Upper bounds: a set meeting every line in 1 to C points, found by a CP-SAT model or CaDiCaL on the plane's incidence
(`src/cap1159.py`; `src/cnf1159.py` for the Hughes plane), or, for PG(2,11) and PG(2,16), as a union of orbits of a
subgroup of the Singer cycle (`src/orbit1159.py`, `src/singer.py`; the point x^i of GF(q^3) is listed by its
coordinates). Lower bounds: if
s points meet every line in 1 to c points, summing (x_ℓ − 1)(c − x_ℓ) ≥ 0 over the lines, with ∑ x_ℓ = s(q + 1) and
∑ x_ℓ(x_ℓ − 1) = s(s − 1), gives s² − (c(q + 1) + 1)s + c(q² + q + 1) ≤ 0, which has no solution for c = 2 (q ≥ 2)
or c = 3 (q ≥ 5); this is the same counting bound as in the plasma-ai/erdos record.

## How it was checked

- Two checkers written separately for this repository: `checks/check1159_a.py` (field tables checked against the
  field axioms, lines from line coordinates, the plane axioms by counting point pairs, and the quadratic inequality)
  and `checks/check1159_b.py` (polynomial arithmetic without tables, lines built as spans of point pairs, files checked
  line against line, and the integer line-type equations ∑ t_i = q² + q + 1, ∑ i t_i = s(q + 1),
  ∑ i(i − 1) t_i = s(s − 1) in place of the inequality). Each rebuilds every plane and every line.
- During the search, each set was also re-checked by the lab's own separate checkers (`check1159.py`,
  `check_singer.py`, not included: they read the lab's file layout).
- No separate referee has reviewed this result yet (the other results in this repository had one).
- Red controls (a point removed, a cap claimed one too small, a reducible field polynomial, a plane file with two
  points swapped) are refused by both checkers.

## Rerun

    sh 1159/checks/run.sh           # Python 3 only, about twenty seconds
