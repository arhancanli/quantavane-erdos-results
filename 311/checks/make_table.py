"""Build the markdown table of delta(N) from program A's verified output (exact fractions)."""
import sys, re, math
from fractions import Fraction as F
rows = []
for line in open(sys.argv[1]):
    m = re.match(r'N=(\d+) delta=(\d+)/(\d+) hits=\d+ set=([\d,]*)', line)
    if not m: continue
    N = int(m.group(1)); d = F(int(m.group(2)), int(m.group(3))); s = m.group(4).rstrip(',')
    rows.append((N, d, s))
print('| N | delta(N) | approx. | -log(delta(N))/N | an optimal set A (sum of 1/a over A is 1 +- delta) |')
print('|---|---|---|---|---|')
for N, d, s in rows:
    if N < 2: continue
    sign = '+' if sum(F(1, int(a)) for a in s.split(',')) > 1 else '-'
    print(f'| {N} | {d.numerator}/{d.denominator} | {float(d):.4e} | {-math.log(float(d))/N:.4f} | {{{s.replace(",", ", ")}}} ({sign}) |')
