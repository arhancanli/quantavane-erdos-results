# Computational results on Erdős Problems #160, #311, #461, #535, #624, #902, #982, #1159 and #1210

Arhan Canli (Quantavane), November 2026. Each result extends work by others, credited first in its section. None of
them settles its problem; each adds checkable facts: computed values or a finite case. Everything here can be
rechecked with `sh checks/run_checks.sh` (Python 3 standard library, about a minute) or
`sh checks/run_checks.sh --full` (also a C compiler; several minutes). Each problem added on 20 November 2026 has its
own folder with a README and its own one-command check, `sh <problem>/checks/run.sh`.

Credits first: each section opens with the earlier work it builds on. Problem statements are those of T. F. Bloom's
[erdosproblems.com](https://www.erdosproblems.com) and of
[google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures).

---

## 1. Erdős Problem #160: h(77) = 7, so h(N) is known for every N ≤ 77

h(N) is the least number of colours of {1, …, N} such that every 4-term arithmetic progression receives at least
3 distinct colours ([#160](https://www.erdosproblems.com/160)). Let M(k) be the largest N with such a k-colouring.

**Credits and what was known.** The repository [scottschluer/erdos160](https://github.com/scottschluer/erdos160)
(October 2026; Zenodo [10.5281/zenodo.23473523](https://doi.org/10.5281/zenodo.23473523)) determined M(3) = 12,
M(4) = 22, M(5) = 35 and M(6) = 53 (the last by 10,067 cubes, each refuted with a checked LRAT certificate) and gave
colourings showing M(7) ≥ 76 and M(8) ≥ 97. So h(N) was known for N ≤ 76, and h(77) was 7 or 8.

**New.** A 7-colouring of {1, …, 77} with every 4-term progression receiving at least 3 colours
(`160/witness/k7_N77.txt`; colours of 1, 2, …, 77 in order):

    1 1 6 2 1 1 0 4 4 6 3 5 3 4 5 2 1 2 0 3 3 4 2 2 5 0 5 6 6 0 4 3 4 6 3 1 5 1 3 5 2 0 2 1 1 0 4 2
    2 5 4 5 6 6 0 4 1 4 6 3 1 5 0 4 0 3 3 1 2 6 2 1 6 2 5 2 0

Hence M(7) ≥ 77 and, with M(6) = 53, h(N) = 7 for 54 ≤ N ≤ 77. The lower bound h(77) ≥ 7 rests on M(6) = 53 from the
repository above; only the colouring is new here.

**Checks.** `160/checks/check160.py` enumerates all 950 progressions; `160/checks/check160_cnf.py` (written separately)
evaluates the 21,644 clauses of the SAT encoding; `160/lean/Erdos160H77.lean` proves the same in Lean 4 (core library,
v4.35.0) by `decide`, with axioms `[propext]` only. All three reject the red controls in `160/controls/` (one position
recoloured, an eighth colour, the 76-colouring with its last colour repeated). `160/src/tabu160b.c` is the tabu search
that found the colouring (seed 10, 3,000,000 iterations, started from the published 76-colouring, kept in
`160/witness/k7_N76_from_scottschluer.txt`, with one random colour appended); it is not needed to check the result.

---

## 2. Erdős Problem #311: δ(N) exactly for every N ≤ 60

δ(N) is the least nonzero value of |1 − Σ_{n∈A} 1/n| over subsets A of {1, …, N}
([#311](https://www.erdosproblems.com/311); Erdős and Graham 1980, p. 40). The question is whether
δ(N) = e^{−(c+o(1))N} for some c in (0, 1).

**Credits and what was known.** The values for N ≤ 25 were posted in the problem's discussion thread on 17 August 2025,
with the observation e^{−0.71N} ≤ δ(N) ≤ e^{−0.52N} for 3 ≤ N ≤ 25 (we compared with the list on the plasma-ai/erdos
page for the problem, which recomputed them). Q. Tang (GitHub note, January 2026) proved
δ(N) ≤ exp(−cN/((log N)^3 (log log N)^3)). We found no computed value for N > 25.

**New.** δ(N) for every 26 ≤ N ≤ 60 with an optimal set for each (`311/results/table.md`). The bound
δ(N) ≤ e^{−0.52N} seen for N ≤ 25 fails for N = 34–37, 39–46, 48–50, 55–57 and 59–60; over 26 ≤ N ≤ 60 the quantity
−log δ(N)/N lies between 0.477 (N = 45) and 0.604 (N = 27). Nothing rigorous about the limit follows. Examples:
δ(36) = 1/33599412, δ(45) = 167/348985892640, δ(51) = 1/2329089562800, δ(60) = 7283/96105030028207200.

**Method and checks.** Exact integer arithmetic over L = lcm(1, …, N) (128-bit; L·H_60 < 2^86): A gives |L − T|/L with
T = Σ L/n. Program A (`311/src/delta_stream_a.c`) stores and sorts the subset sums of the top ⌊N/2⌋ (at most 26)
numbers, streams the rest in Gray-code order and binary-searches the nearest sums to L − x, skipping exact hits.
Program B (`311/src/delta_merge_b.c`, written separately) splits off the even numbers 2, 4, … instead and matches by a
two-pointer sweep. They agree on all 60 values (`311/results/A_1_60.txt`, `B_1_60.txt`). `311/checks/verify_311.py`
checks with exact fractions that each listed set attains its value, that the value is nonzero, that A and B agree,
that δ is non-increasing and that N ≤ 25 matches the published list; it rejects the red controls in `311/controls/`.
`311/checks/brute_small.py` enumerates all 2^N subsets directly and agrees for N ≤ 20. A and B are independent code but
the same method; the brute force and the published N ≤ 25 values are the method-independent checks.

---

## 3. Erdős Problem #902: no Cayley tournament on fewer than 67 vertices has property S_4

A tournament has property S_k if every k vertices have a common dominator ([#902](https://www.erdosproblems.com/902);
Erdős 1963). f(k) is the least order of an S_k tournament: f(1) = 3, f(2) = 7, f(3) = 19, and 48 ≤ f(4) ≤ 67
(lower bound: Reid, McRae, Hedetniemi and Hedetniemi 2004, Corollary 7; upper bound: the Paley tournament on 67
vertices, Graham and Spencer 1971; 67 is the least Paley order with S_4, OEIS A362137).

**Credits and what was known.** The repository [jaredwilder/erdos902](https://github.com/jaredwilder/erdos902)
(2026) showed that no circulant tournament of odd order 33 to 45 has S_4, eliminated both Cayley families of order 49
(on Z_49 and Z_7²) with checked DRAT certificates, and recorded the circulant cases 49 and 65 as unresolved.

**New.** Every Cayley tournament of order below 67 fails S_4. Cayley tournaments have odd order (an involution g makes
the pair {e, g} impossible to orient consistently). Orders up to 46 are excluded by the Szekeres–Szekeres bound
f(4) ≥ 47. For every group of odd order 47 to 65 — Z_47, Z_49, Z_7², Z_51, Z_53, Z_55, Z_11 ⋊ Z_5, Z_57, Z_19 ⋊ Z_3,
Z_59, Z_61, Z_63, Z_3 × Z_21, Z_7 ⋊ Z_9, Z_3 × (Z_7 ⋊ Z_3), Z_65; that these are all groups of these orders is the
standard classification — all 2^((n−1)/2) Cayley tournaments were checked, with no symmetry reduction. With the Paley
tournament, 67 is the least order of a Cayley S_4 tournament; on 67 vertices the only circulant S_4 tournaments are
the Paley tournament and its reverse, which is isomorphic to it (`circ_s4` and `cayley_sk128` both find exactly these
two of the 2^33). This does not improve f(4) ≤ 67.

**Method and checks.** In a Cayley tournament (x → y iff x⁻¹y ∈ D) left translations act transitively, so it is enough
that every 4-set containing the identity e has a dominator; v dominates S iff v ∈ s·D⁻¹ for every s in S.
`902/src/circ_s4.c` (cyclic groups; rotations of a 128-bit mask), `902/src/cayley_sk128.c` (any group from its
multiplication table; Gray code with incremental updates) and `902/src/cayley_direct.c` (written separately; plain
counter, translates computed when needed) agree: no S_4 tournament in any of the 16 groups (`902/results/*.log`).
Controls: the Paley set on Z_67 passes and the one on Z_59 fails in every program and in the brute-force checker
`902/checks/check_sk.py`; reversing one arc of the 67-vertex Paley tournament breaks S_4; the numbers of circulant S_3
tournaments agree between programs (0, 2, 80, 234, 816, 2462, 6684, 20032, 50352 for n = 21..37; 8,699,474 for n = 49;
18,001,792 for n = 51). `902/src/make_groups.py` writes the 17 group tables in `902/groups/`, and
`902/checks/group_invariants.py` re-checks the group axioms and shows the tables are pairwise non-isomorphic.
Historical note on the logs: a 64-bit build of `cayley_sk` was used for n ≤ 61 (safe there) and replaced by the
128-bit one; the sweep of `cayley_direct` ran a build whose 32-bit cache stamp wrapped on the very last candidate of
Z_65 only, and that candidate was rechecked with the build in `src/`.

---

## 4. Erdős Problem #461: the minimum of f(n,t) over n, exactly, for t ≤ 54 and even t ≤ 64 ([461/](461/))

f(n,t) is the number of distinct t-smooth parts of n+1, …, n+t. Building on the reduction recorded on the
plasma-ai/erdos page for the problem (f depends only on n mod ∏_{p<t} p^{e_p}; minima there for t = 2, 3), the exact
minimum m(t) over all n: m(t) = ⌊t/2⌋ + 1 for 4 ≤ t ≤ 43, t = 45, 53; ⌊t/2⌋ for t = 44, 46–52, 54, 56; t/2 − 1 for
t = 58, …, 64; and explicit n with f(n,2560) = 1004 = 0.392 t. Two exhaustive programs, a referee's third, and an
explicit n for every value.

---

## 5. Erdős Problem #535: f_3(N) exactly for every N ≤ 64 ([535/](535/))

f_3(N) is the largest subset of {1, …, N} with no three elements of equal pairwise gcds (bounds: Erdős 1964,
Abbott–Hanson 1970). Values 1, 2, 2, 3, 3, 3, 3, 4, 5, …, rising to 12 at N = 54–64, with an optimal set for each N.
Two exact programs (integer programming; CP-SAT), a referee's SAT certificates and branch and bound, and a plain
exhaustive search in this repository.

---

## 6. Erdős Problem #624: H(n) for n = 2, …, 11 ([624/](624/))

For the statement with f arbitrary (formal-conjectures), H(n) = 1, 2, 3, 3, 3, 4, 4, 4, 4, 4 (bounds: Erdős–Hajnal
1968; Alon). Explicit f for every upper bound; lower bounds by counting, by LRAT-certified unsatisfiability (n = 4, 7)
and by monotonicity. Small cases may have been discussed in the problem's forum thread; see the folder.

---

## 7. Erdős Problem #982 for every n ≤ 13, in Lean ([982/](982/))

Every convex n-gon with 3 ≤ n ≤ 13 has a vertex with ⌊n/2⌋ distinct distances. These cases were settled before us
(Paulee314/erdos982, 2 November 2026, Zenodo 10.5281/zenodo.23880465; n = 8 by Fishburn); what is offered is a Lean 4
proof in formal-conjectures' form, in [arhancanli/quantavane-lean](https://github.com/arhancanli/quantavane-lean)
(it trusts `native_decide` for the LRAT checks). The folder re-checks those LRAT steps and the n = 12 angle
certificate without Lean.

---

## 8. Erdős Problem #1159: the least cap of a blocking set in twelve small planes ([1159/](1159/))

The least C such that some point set meets every line in 1 to C points: 3 for PG(2,2), PG(2,3), PG(2,4); 4 for
PG(2,5), PG(2,7), PG(2,8), PG(2,9), PG(2,11), PG(2,16) and the Hall, dual Hall and Hughes planes of order 9. The lower
bounds use the counting bound recorded on the plasma-ai/erdos page, which also had cap-4 sets for q = 5, 7, 11;
Bruen–Fisher's construction already gives cap 4 in PG(2,9), and Baer subplanes give cap 3 in PG(2,4) and cap 4 in all
four planes of order 9. New as far as we could find: PG(2,8) and PG(2,16). Two checkers and a referee's own programs.

---

## 9. Erdős Problem #1210: M(n) exactly for every 3 ≤ n ≤ 1794 ([1210/](1210/))

M(n) is the largest ∑ 1/(n − a) over pairwise coprime A ⊆ [1, n). Complementing E. Li (arXiv:2606.17955: average
order and almost-all results, no table), M(n) as an exact fraction with a maximiser for every n ≤ 1794; the excess
E(n) = M(n) − ∑_{p<n} 1/p equals 1 at n = 3, 4, 6 and stays below 1 for every other n in this range (largest: 0.9695 at n = 204). Branch and
bound, an integer programme, and a referee's exact dynamic programme over every n.

---

## Rerun everything

    sh checks/run_checks.sh            # quick: about a minute, Python 3 only
    sh checks/run_checks.sh --full     # also compiles and reruns the C programs and the Lean file (several minutes)
    sh 461/checks/run.sh               # one problem only (also 535, 624, 982, 1159, 1210; each takes --full)

Full reruns: #311 `for N in $(seq 1 60); do ./a $N; done` (N = 60 takes about 15 minutes and 1.1 GB for A, a few
minutes and 1.6 GB for B); #902 `./circ_s4 n 4` for odd n and `./cayley_sk128 902/groups/group_X.txt 4`,
`./cayley_direct 902/groups/group_X.txt` (about an hour in all on one core). `SHA256SUMS` lists every file.

## How AI was used

The programs, the checkers, the Lean files and the READMEs were written with Claude (Anthropic), directed by
Arhan Canli. The referees named in the folders are separate Claude sessions that were given only the claim, the
lemmas and the programs, and wrote their own programs from the definitions. The results rest on explicit objects
(colourings, optimal sets, functions, point sets, certificates) and on programs and checkers that anyone can rerun
from this repository; nothing here depends on the AI's judgement.

## Licence and citation

Text and data (colourings, tables, witnesses, certificates, logs): CC BY 4.0 (`LICENSE`), except the third-party
files named there. Programs and the Lean file: MIT (`LICENSE-CODE`).
Please cite as: Arhan Canli, Computational results on Erdős problems, Quantavane, 2026,
https://github.com/arhancanli/quantavane-erdos-results, together with the work credited above.
