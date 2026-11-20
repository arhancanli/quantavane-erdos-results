"""LRAT proof checker (Python 3 standard library; written for this repository, separately from checks/lratcheck.c).

Usage: python3 lrat_check.py FORMULA.cnf[.gz] PROOF.lrat[.gz]

The formula's clauses get the ids 1..m in file order. Every addition step "id lits 0 hints 0" must be a reverse unit
propagation (RUP) step: assume every literal of the new clause false, then each hint, in order, must name a live clause
that is unit (its one unassigned literal is then set true) until a hint is falsified outright. Deletion steps
"id d ids 0" remove clauses. RAT steps (negative hints) are refused; so are a hint to a missing or deleted clause, a hint
that is already satisfied or has two unassigned literals, a reused id, and a step that ends without a conflict.
Prints "s VERIFIED UNSAT" and exits 0 only if the empty clause is derived."""
import gzip
import sys


def opener(path):
    return gzip.open(path, 'rt') if path.endswith('.gz') else open(path)


def fail(msg):
    print('s NOT VERIFIED (%s)' % msg)
    sys.exit(1)


def read_cnf(path):
    db, cur, header = {}, [], None
    with opener(path) as f:
        for line in f:
            tok = line.split()
            if not tok or tok[0] == 'c':
                continue
            if tok[0] == 'p':
                header = (int(tok[2]), int(tok[3]))
                continue
            for t in tok:
                x = int(t)
                if x == 0:
                    db[len(db) + 1] = tuple(cur)
                    cur = []
                else:
                    cur.append(x)
    if cur:
        fail('formula ends inside a clause')
    if header is None or header[1] != len(db):
        fail('formula has %d clauses, header says %s' % (len(db), header))
    return db


def rup(lits, hints, db):
    true = set()
    for l in lits:
        if l in true:
            continue
        if -l in true:
            return False, 'tautology'
        true.add(-l)
    for h in hints:
        if h <= 0:
            return False, 'RAT hint %d (not supported)' % h
        c = db.get(h)
        if c is None:
            return False, 'hint %d is not a live clause' % h
        free = None
        nfree = 0
        for l in c:
            if l in true:
                return False, 'hint %d is satisfied' % h
            if -l not in true:
                nfree += 1
                free = l
        if nfree == 0:
            return True, ''
        if nfree > 1:
            return False, 'hint %d is not unit' % h
        true.add(free)
    return False, 'no conflict after the hints'


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    db = read_cnf(sys.argv[1])
    m = len(db)
    adds = dels = 0
    with opener(sys.argv[2]) as f:
        for lineno, line in enumerate(f, 1):
            tok = line.split()
            if not tok or tok[0] == 'c':
                continue
            cid = int(tok[0])
            if tok[1] == 'd':
                for t in tok[2:]:
                    x = int(t)
                    if x == 0:
                        break
                    db.pop(x, None)
                dels += 1
                continue
            nums = [int(t) for t in tok[1:]]
            if nums.count(0) != 2 or nums[-1] != 0:
                fail('line %d is not "id lits 0 hints 0"' % lineno)
            z = nums.index(0)
            lits, hints = nums[:z], nums[z + 1:-1]
            if cid in db or cid <= m:
                fail('line %d reuses id %d' % (lineno, cid))
            ok, why = rup(lits, hints, db)
            if not ok:
                fail('line %d, step %d: %s' % (lineno, cid, why))
            adds += 1
            if not lits:
                print('c formula: %d clauses; checked %d additions, %d deletion lines' % (m, adds, dels))
                print('s VERIFIED UNSAT')
                return
            db[cid] = tuple(lits)
    fail('the empty clause was not derived')


if __name__ == '__main__':
    main()
