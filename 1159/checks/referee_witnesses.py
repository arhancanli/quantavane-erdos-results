"""Referee check of every set in results/witnesses.json (Erdos #1159), written by a separate session from the
definitions, without reading the lab's code. Python 3 standard library.

Usage: python3 -I referee_witnesses.py results/witnesses.json [--alt]
  (--alt builds GF(8), GF(9), GF(16) from t^3+t+1, t^2+1, t^4+t+1 instead of t^3+t^2+1, t^2+t+2, t^4+t^3+1)

PG(2,q) is built from the referee's own field (referee_rplane.py). A witness coordinate, an integer label n of the
lab's field, is carried into the referee's field by n = sum d_i p^i  ->  sum d_i r^i, where r is a root in the
referee's field of the lab's printed modulus (read constant term first; the other reading is also tried and
reported). That map is a field isomorphism, so a set that passes is a valid set of PG(2,q).
The planes of order 9 are read from the files in planes/ (G. E. Moorhouse's lists), points as labels.
For every set: all points distinct, every line load in 1..C, sum of loads = s(q+1), sum of load(load-1) = s(s-1),
and the counting lemma excludes C - 1. Red controls, which must fail: the same set with cap C - 1, and the set with
its smallest point replaced by the smallest point outside it. Exits non-zero on any failure.
"""
import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import referee_rplane as R  # noqa


def lemma_excludes(q, C):
    return not any(R.counting_bound_ok(s, q, C) for s in range(q * q + q + 2))


def check_set(lines, S, q, C):
    L = R.loads(lines, S)
    s = len(S)
    return (len(set(S)) == s and min(L) >= 1 and max(L) <= C and sum(L) == s * (q + 1)
            and sum(x * (x - 1) for x in L) == s * (s - 1)), min(L), max(L)


def red_ok(lines, S, n_points, q, C):
    """True if both red controls are refused."""
    if check_set(lines, S, q, C - 1)[0]:
        return False
    outside = [x for x in range(n_points) if x not in set(S)]
    if not outside:  # the set is the whole plane (PG(2,2)): only the cap control applies
        return True
    first = sorted(S)[0]
    return not check_set(lines, [x for x in S if x != first] + [outside[0]], q, C)[0]


def irreducible(cf, p):
    h = len(cf) - 1

    def rem(a, b):
        a = list(a)
        while len(a) >= len(b):
            k = a[-1] * pow(b[-1], p - 2, p) % p
            if k:
                for i, bc in enumerate(b):
                    a[len(a) - len(b) + i] = (a[len(a) - len(b) + i] - k * bc) % p
            a.pop()
        return a
    return all(any(rem(cf, list(low) + [1])) for d in range(1, h // 2 + 1)
               for low in itertools.product(range(p), repeat=d))


def main():
    wpath = sys.argv[1]
    if "--alt" in sys.argv:
        R.REF_MODULI.update(R.ALT_MODULI)
    planes_dir = os.path.join(os.path.dirname(os.path.abspath(wpath)), "..", "planes")
    W = json.load(open(wpath))
    bad = 0
    for w in W:
        q, C = w["q"], w["C"]
        lem = lemma_excludes(q, C - 1)
        if "file" in w:
            lines = R.read_moorhouse(os.path.join(planes_dir, os.path.basename(w["file"])))
            R.verify_plane(lines, q)
            S = list(w["points"])
            ok, lo, hi = check_set(lines, S, q, C)
            red = red_ok(lines, S, len(lines), q, C)
            how = "Moorhouse file"
        else:
            F = R.Field(q)
            F.verify_axioms()
            P = R.PG2(F)
            R.verify_plane(P.lines, q)
            maps = []
            if w.get("modulus") is None:
                maps.append(("prime field", list(range(q))))
            else:
                p, h = w["p"], w["h"]
                for name, cf in (("modulus constant-first", list(w["modulus"])),
                                 ("modulus leading-first", list(reversed(w["modulus"])))):
                    if cf[-1] != 1 or len(cf) != h + 1 or not irreducible(cf, p):
                        continue
                    for r in range(q):
                        if F.eval_poly(cf, r) == 0:
                            phi = []
                            for n in range(q):
                                acc, rp = 0, 1
                                for d in R.digits(n, p, h):
                                    acc = F.add[acc][F.mul[d][rp]]
                                    rp = F.mul[rp][r]
                                phi.append(acc)
                            assert sorted(phi) == list(range(q))
                            maps.append(("%s, t -> %d" % (name, r), phi))
            if not maps:
                bad += 1
                print("FAIL %-27s q=%-2d no usable reading of the modulus (not monic of degree h, or reducible)"
                      % (w["plane"], q))
                continue
            results = []
            for name, phi in maps:
                S = [P.index[P.normalise(tuple(phi[x] for x in v))] for v in w["points"]]
                ok1, lo1, hi1 = check_set(P.lines, S, q, C)
                results.append((name, ok1, lo1, hi1, ok1 and red_ok(P.lines, S, len(P.points), q, C)))
            passing = [r for r in results if r[1]]
            ok = bool(passing) and all(r[1] for r in results if r[0].startswith("prime") or
                                       r[0].startswith("modulus constant-first"))
            lo, hi = (passing[0][2], passing[0][3]) if passing else (results[0][2], results[0][3])
            red = all(r[4] for r in passing)
            how = "; ".join("%s: %s" % (r[0], "pass" if r[1] else "fail (loads %d..%d)" % (r[2], r[3]))
                            for r in results)
        good = ok and lem and red
        bad += not good
        print("%s %-27s q=%-2d C=%d |S|=%-2d loads %d..%d  C-1 excluded=%s  red controls refused=%s  [%s]"
              % ("PASS" if good else "FAIL", w["plane"], q, C, len(w["points"]), lo, hi, lem, red, how))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
