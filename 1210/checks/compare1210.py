"""Compares program output lines "n=<n> M=<fraction> ..." (src/bnb1210.py, src/brute1210.py) with results/table.txt.
Every n in the output must be in the table with exactly the same M(n). Exits non-zero otherwise; prints the count.
Usage: python3 compare1210.py table.txt output.txt"""
import re
import sys
T = {}
for line in open(sys.argv[1]):
    t = line.split()
    if t and not t[0].startswith('#'):
        T[int(t[0])] = t[1]
n_ok, bad = 0, []
for line in open(sys.argv[2]):
    m = re.match(r'n=(\d+) M=(\S+)', line)
    if m:
        if T.get(int(m.group(1))) == m.group(2):
            n_ok += 1
        else:
            bad.append(int(m.group(1)))
print('%d rows equal the table, %d differ%s' % (n_ok, len(bad), (': ' + str(bad[:10])) if bad else ''))
sys.exit(1 if bad or n_ok == 0 else 0)
