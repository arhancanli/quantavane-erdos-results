"""Checks certificates/cuts12_images.json for Erdős #982, n = 12 (Python 3 standard library; written for this
repository). The Lean proof adds one cut clause per entry of that file; each entry must be the image of the five base
equalities |p8 p5| = |p8 p6|, |p8 p10| = |p8 p11|, |p10 p7| = |p10 p8|, |p11 p4| = |p11 p6|, |p11 p5| = |p11 p8| (the
first entry, ["E", o, a, b] meaning |p_o p_a| = |p_o p_b|) under one of the 24 dihedral maps i -> s + i or s - i
(mod 12), and every one of the 24 images must occur exactly once. Exits non-zero otherwise.
Usage: python3 check_cuts12.py cuts12_images.json"""
import json
import sys

n = 12
E = json.load(open(sys.argv[1]))
norm = lambda rel: tuple(sorted((o, min(a, b), max(a, b)) for _, o, a, b in rel))
base = E[0]
images = []
for refl in (1, -1):
    for s in range(n):
        g = lambda i: (s + refl * i) % n
        images.append(norm([['E', g(o), g(a), g(b)] for _, o, a, b in base]))
given = [norm(rel) for rel in E]
ok = len(E) == 24 and len(set(images)) == 24 and sorted(given) == sorted(images)
print('%s %d entries; the 24 dihedral images of the base equalities are distinct and each occurs once: %s'
      % ('PASS' if ok else 'FAIL', len(E), ok))
sys.exit(0 if ok else 1)
