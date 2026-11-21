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
- Baer subplanes: in a plane of order q = m², a subplane of order m meets every line in 1 or m + 1 points (a
  classical fact; R. H. Bruck, 1955). So a Baer subplane is a cap-3 set in PG(2,4) and a cap-4 set in a plane of
  order 9 (the plasma-ai/erdos record notes this for PG(2,9)). Each of the four planes of order 9 has one (the Hughes
  plane contains PG(2,3) by its construction; the referee also found one in each of Moorhouse's files with
  `checks/referee_baer.py`). With the counting bound, c = 3 for PG(2,4) and c = 4 for all four planes of order 9 follow
  from these known facts; the sets listed here are other sets with the same caps.
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

So all four planes of order 9 have least cap 4 (as their Baer subplanes already show), and PG(2,8) and PG(2,16) have
least cap 4, below the 5 or 6 of the general constructions for PG(2,2^r). The sets are in `results/witnesses.json`
(points of PG(2,q) as coordinate triples over GF(q), with the field's defining polynomial; points of the other planes
as numbers in Moorhouse's files). An element of GF(p^h) is written as the integer ∑ c_i p^i, standing for ∑ c_i t^i,
and `modulus` lists the coefficients of the defining polynomial constant term first: [1, 0, 1, 1] is 1 + t² + t³ for
GF(8), [1, 0, 0, 1, 1] is 1 + t³ + t⁴ for GF(16). (Read the other way round, the GF(8) and GF(16) sets fail.)
PG(2,13) and PG(2,17) are not decided here, and nothing here bears on large orders.

## New and known

- Known before this repository: c = 3 for PG(2,2) (a line meets every other line once) and for PG(2,4) (a Baer
  subplane); c = 4 for PG(2,5), PG(2,7) and PG(2,11) (plasma-ai/erdos), for PG(2,9) (a Baer subplane; Bruen and
  Fisher) and, by Baer subplanes and the counting bound, for the Hall, dual Hall and Hughes planes of order 9. The
  lower bounds are the counting bound of the plasma-ai/erdos record.
- Elementary, not found stated: c = 3 for PG(2,3) (a 6-point set; there are 468 sets with cap 3 among all 2^13
  subsets).
- New as far as we could find: c = 4 for PG(2,8) and for PG(2,16). The constructions read give 5 or 6 for PG(2,2^r)
  (Illés, Szőnyi and Wettl; three conics on plasma-ai/erdos), and 5 for PG(2,16) (a Baer subplane or a unital).
- Searched (21 Nov 2026): the plasma-ai/erdos record and lead page for #1159; S. Asgarli, D. Ghioca and C. H. Yip,
  Blocking sets from a union of plane curves (arXiv:2510.15332v2); A. Blokhuis, Combinatorial problems in finite
  geometry and lacunary polynomials (ICM 2002, arXiv:math/0304463); OpenAlex, including the works citing
  Erdős–Silverman–Stein (1983) and Ughi (1988). Not read: H. L. Abbott and A. Liu, Property B(s) and projective planes
  (Ars Combin. 20, 1985); R. Silverman and A. Stein (Int. J. Comput. Geom. Appl. 2, 1992); E. Ughi (Geom. Dedicata 26,
  1988); Illés, Szőnyi and Wettl (1991); A. Gács and T. Szőnyi (Des. Codes Cryptogr. 47, 2008). Any of these may hold
  small cases.

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
- Referee (21 Nov 2026): a separate AI session, given only the claim and the files, wrote its own field, plane and
  checking code from the definitions (`checks/referee_rplane.py`, `checks/referee_witnesses.py`: GF(8), GF(9) and
  GF(16) built from its own polynomials, each set carried over by a field isomorphism; the planes of order 9
  downloaded again from Moorhouse's site, byte-identical), and its own exhaustive searches (`checks/referee_exh.c`,
  `checks/referee_brute.c`, `checks/referee_exhaustive.py`): no cap-3 set in PG(2,5) by brute force over all 2^31
  subsets and by a search without symmetry breaking, none in PG(2,7) with and without symmetry breaking, and least
  cap 3 for q ≤ 4 by brute force. It also found a Baer subplane in each plane of order 9 (`checks/referee_baer.py`),
  and an invariant (quadrangles with collinear diagonal points; `checks/referee_fano.c`) shows that the four planes
  of order 9 used here are pairwise non-isomorphic (the Hall and dual Hall files give the same counts with points
  and lines swapped, as a plane and its dual must).
  Verdict: correct, with fixes to the credits (Baer subplanes) and to the description of the field encoding, both made
  above; no value changed.
- Red controls (a point removed, a cap claimed one too small, a reducible field polynomial, a plane file with two
  points swapped) are refused by both checkers.

## Rerun

    sh 1159/checks/run.sh           # Python 3 only, about twenty seconds
    sh 1159/checks/run.sh --full    # also the referee's programs (needs a C compiler; about a minute)
