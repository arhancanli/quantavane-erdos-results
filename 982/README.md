# Erdős Problem #982: every convex n-gon with n ≤ 13 has a vertex with ⌊n/2⌋ distinct distances, in Lean

A finite case (3 ≤ n ≤ 13); not a solution of the problem. The cases themselves were settled before us (below); what
is offered here is a Lean 4 proof of them in the form formal-conjectures states the problem.

## The problem

As stated in [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
(`FormalConjectures/ErdosProblems/982.lean`, theorem `Erdos982.erdos_982`;
[erdosproblems.com/982](https://www.erdosproblems.com/982)): if n ≥ 3 distinct points in ℝ² form a convex polygon,
then some vertex has at least ⌊n/2⌋ different distances to the other vertices. The regular n-gon shows that ⌊n/2⌋
cannot be raised.

## Credits and what was known

- Every n ≤ 13 was settled by computer in [Paulee314/erdos982](https://github.com/Paulee314/erdos982)
  (2 November 2026; proofs on Zenodo, [doi:10.5281/zenodo.23880465](https://doi.org/10.5281/zenodo.23880465)), with
  the solver proofs checked by the verified checker cake_lpr; n = 8 is in print in Fishburn, "Distances in convex
  polygons" (The Mathematics of Paul Erdős I, Springer), Theorem 3. We found this earlier work after our first
  publication and corrected our description then.
- General bounds for the number of distances guaranteed at some vertex: ⌈n/3⌉ (Moser 1952), ⌊n/3⌋ + 1 (Erdős and
  Fishburn 1994), ⌈(13n − 6)/36⌉ (Dumitrescu 2006), (13/36 + 1/22701)n − O(1) (Nivasch, Pach, Pinchasi and Zerbib
  2013). The concyclic case is proved in Lean in arex1337/formal-conjectures-proofs (linked from formal-conjectures).

## What is proved

`E982C.erdos_982_le_thirteen` in the public repository
[arhancanli/quantavane-lean](https://github.com/arhancanli/quantavane-lean/tree/19426bfa8c21a97c2021db4841c4f2984d459f47/erdos982-le13)
(commit 19426bf, folder `erdos982-le13`) has, for every 3 ≤ n ≤ 13, exactly the type of formal-conjectures'
`Erdos982.erdos_982 n` (checked there with `type_of%` in `test/Statement12.lean`). The proof uses no `sorry`; it
depends on the axioms `propext`, `Classical.choice`, `Quot.sound` and on the `native_decide` axioms of its LRAT checks,
so it trusts Lean's compiler for those evaluations. Because of `native_decide` it is not eligible for the Palomar
registry as it stands.

## Method

Lean itself writes, from geometric lemmas proved in Lean (orientation and distance facts of convex polygons: a
half-plane rule for equal and shorter distances, and a bound on acute angles), a CNF that the distance pattern of any
counterexample would satisfy, and Lean's verified LRAT checker checks a SAT solver's refutation of it. For n = 12 one
more fact is needed: five particular equal distances in a convex 12-gon would force a weighted sum of 71 angle
equations to exceed what the angles allow by 45 degrees; Lean proves this for all 24 dihedral images, and the
refutation with these 24 extra clauses (2,505,174 lemmas after trimming) is checked inside Lean in ten chunks.

## How it was checked

- In Lean: the whole proof, rebuilt from scratch in a separate copy with every module of the project deleted first,
  before the statement and the axioms were printed.
- Outside Lean: n ≤ 11 also by a second, separately written encoding of the lemmas and three SAT solvers, with
  controls that are satisfiable where they should be; n = 13 by a second encoding written in Python; the LRAT
  proofs by drat-trim's lrat-check and by our own C checker; the n = 12 angle certificate re-derived exactly from the
  definitions by a second program (`checks/check_angle12.py`), with a control that fails.
- This folder holds what can be re-checked without Lean, in seconds: the CNFs that Lean writes for n = 4, 6, 8, 10
  (`lake exe dumpc n K` in the Lean project; SHA-256 checked) with the LRAT proofs Lean checks
  (`certificates/lrat/`, which also cover n = 5, 7, 9, 11 through the odd-n step), checked again by two separately
  written LRAT checkers (`../checks/lrat_check.py` in Python, `../checks/lratcheck.c` in C); the n = 12 angle
  certificate (`certificates/core1.cert`, exact rational arithmetic, all 24 images) and its 24 cut images
  (`certificates/cuts12_images.json`, `checks/check_cuts12.py`). The n = 12 and n = 13 proofs are 2.0 GB and 234 MB;
  `lrat/make_12.sh` and `make_13.sh` in the Lean project regenerate them and check their SHA-256.
- Red controls: a truncated proof, a proof with one hint removed, the angle certificate with a multiplier doubled or
  one equality removed, and a repeated cut image are refused.

## Rerun

    sh 982/checks/run.sh            # Python 3 only, a few seconds
    sh 982/checks/run.sh --full     # also the C LRAT checker
    # the full proof: build erdos982-le13 in arhancanli/quantavane-lean as its README describes (Lean v4.33.1, Mathlib)
