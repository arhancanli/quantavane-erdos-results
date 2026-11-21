"""Referee's exhaustive searches for Erdos #1159 (separate session, own code), run with the C programs
referee_exh.c and referee_brute.c on planes built by referee_rplane.py.

Usage: python3 -I referee_exhaustive.py <path to compiled referee_exh> <path to compiled referee_brute> [--with-q5-brute]

Expected (exit non-zero otherwise):
  q = 2, 3, 4: brute force over every subset gives least cap 3, and referee_exh (point mode) counts the same
               number of cap-3 sets as the brute force; no cap-2 set.
  q = 5: no cap-3 set: referee_exh point mode (all 2^31 subsets implicitly, no symmetry breaking) and line mode;
         with --with-q5-brute also the plain brute force over all 2^31 subsets (about half a minute).
  q = 7: no cap-3 set: referee_exh line mode with no symmetry breaking, and with the frame
         (1,0,0), (0,1,0), (0,0,1), (1,1,1) forced in. The frame is a valid normalisation: if S meets every line
         of PG(2,7) in 1..3 points, then |S| >= 8 (the 8 lines through a point off S each hold a point of S), S is
         not inside one line, and if no four points of S were in general position, S would lie on the three
         sides of a triangle of its points, so |S| <= 3*3 - 3 = 6. So S contains a quadrangle, and PGL(3,7) is
         transitive on ordered quadrangles.
  green controls: line mode finds a cap-3 set in PG(2,4) and cap-4 sets in PG(2,5), PG(2,7), PG(2,8), PG(2,9),
         each re-checked here.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import referee_rplane as R  # noqa


def plane(q):
    F = R.Field(q)
    F.verify_axioms()
    P = R.PG2(F)
    R.verify_plane(P.lines, q)
    return P


def text(P, forced=()):
    rows = ["%d %d %d" % (len(P.points), len(P.lines), len(P.lines[0]))]
    rows += [" ".join(map(str, L)) for L in P.lines]
    rows.append("%d %s" % (len(forced), " ".join(map(str, forced))))
    return "\n".join(rows) + "\n"


def run(prog, args, txt):
    out = subprocess.run([prog] + args, input=txt, capture_output=True, text=True, check=True).stdout
    return out


def main():
    exh, brute = sys.argv[1], sys.argv[2]
    bad = 0

    def report(ok, msg):
        nonlocal bad
        bad += not ok
        print("%s %s" % ("ok  " if ok else "FAIL", msg))

    for q in (2, 3, 4):
        P = plane(q)
        b = run(brute, [], text(P))
        cap3 = int([x for x in b.splitlines() if x.startswith("C=3 ")][0].split()[-1])
        least = int(b.splitlines()[-1].split()[-1])
        n2 = int(run(exh, ["2", "point"], text(P)).split()[4])
        n3 = int(run(exh, ["3", "point"], text(P)).split()[4])
        report(least == 3 and n2 == 0 and n3 == cap3,
               "PG(2,%d): brute force least cap %d; cap-3 sets: brute %d, exh %d; cap-2 sets: exh %d"
               % (q, least, cap3, n3, n2))
    P = plane(5)
    n = int(run(exh, ["3", "point"], text(P)).split()[4])
    r = run(exh, ["3", "line"], text(P)).split()[3]
    report(n == 0 and r == "UNSAT", "PG(2,5): no cap-3 set (point mode %d solutions, line mode %s)" % (n, r))
    if "--with-q5-brute" in sys.argv:
        b = run(brute, [], text(P))
        least = int(b.splitlines()[-1].split()[-1])
        report(least == 4, "PG(2,5): brute force over all 2^31 subsets gives least cap %d" % least)
    P = plane(7)
    fr = [P.index[v] for v in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]]
    r1 = run(exh, ["3", "line"], text(P)).split()[3]
    r2 = run(exh, ["3", "line"], text(P, fr)).split()[3]
    report(r1 == "UNSAT" and r2 == "UNSAT",
           "PG(2,7): no cap-3 set (line mode, no symmetry breaking: %s; frame forced: %s)" % (r1, r2))
    for q, C in ((4, 3), (5, 4), (7, 4), (8, 4), (9, 4)):
        P = plane(q)
        out = run(exh, [str(C), "line"], text(P))
        S = [int(x) for x in [x for x in out.splitlines() if x.startswith("S:")][0][2:].split()]
        L = R.loads(P.lines, S)
        report(min(L) >= 1 and max(L) <= C, "green control PG(2,%d): a cap-%d set of size %d found and checked"
               % (q, C, len(S)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
