/* Referee program for #535, second method (no solver): exact branch and bound over subsets of {1..N}, N <= 64.
   forb[a][b] = bitmask of c with {a,b,c} forbidden, computed from the definition (three pairwise gcds equal).
   Branch on the largest remaining candidate x: include x (then remove every c that would complete a forbidden triple
   with x and an already chosen a), or exclude x. Bound: |chosen| + |candidates| plus a clique bound: candidates are
   greedily packed into groups in which every 3-subset is forbidden (so each group holds at most 2 chosen elements).
   Usage: referee_535_bnb N0 N1  -> prints N, f_3(N), one optimal set (re-checked by brute force). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t u64;
static int N, best, bestset[65], cur[65];
static u64 forb[65][65];
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int bad3(int a, int b, int c) { int g = gcd(a, b); return gcd(a, c) == g && gcd(b, c) == g; }
static int pc(u64 m) { return __builtin_popcountll(m); }
static int cliquebound(u64 cand) {
  /* greedy: take the largest x, build a group G containing x where all triples are forbidden (needs every pair in G
     to complete a forbidden triple with every third member); each group contributes min(|G|,2). */
  int tot = 0;
  while (cand) {
    int x = 63 - __builtin_clzll(cand) + 1; u64 G = 1ULL << (x - 1); cand &= ~G;
    int mem[65], k = 0; mem[k++] = x;
    u64 c2 = cand;
    while (c2 && k < 64) {
      int y = 63 - __builtin_clzll(c2) + 1; c2 &= ~(1ULL << (y - 1));
      /* y joins only if every triple it forms with two current members is forbidden (vacuous when k == 1) */
      int ok = 1;
      for (int i = 0; i < k && ok; i++) for (int j = i + 1; j < k && ok; j++) if (!bad3(mem[i], mem[j], y)) ok = 0;
      if (ok) { mem[k++] = y; G |= 1ULL << (y - 1); }
    }
    cand &= ~G; tot += k < 2 ? k : 2;
  }
  return tot;
}
static void dfs(u64 cand, int size) {
  if (size > best) { best = size; for (int i = 0; i < size; i++) bestset[i] = cur[i]; }
  if (!cand) return;
  if (size + pc(cand) <= best) return;
  if (size + cliquebound(cand) <= best) return;
  int x = 63 - __builtin_clzll(cand) + 1; u64 rest = cand & ~(1ULL << (x - 1));
  u64 kill = 0; for (int i = 0; i < size; i++) kill |= forb[cur[i]][x];
  cur[size] = x; dfs(rest & ~kill, size + 1);
  dfs(rest, size);
}
int main(int argc, char **argv) {
  int N0 = atoi(argv[1]), N1 = atoi(argv[2]);
  for (N = N0; N <= N1; N++) {
    for (int a = 1; a <= N; a++) for (int b = 1; b <= N; b++) { forb[a][b] = 0;
      if (a != b) for (int c = 1; c <= N; c++) if (c != a && c != b && bad3(a, b, c)) forb[a][b] |= 1ULL << (c - 1); }
    best = 0; u64 all = (N == 64) ? ~0ULL : ((1ULL << N) - 1);
    dfs(all, 0);
    int ok = 1;
    for (int i = 0; i < best; i++) for (int j = i + 1; j < best; j++) for (int k = j + 1; k < best; k++)
      if (bad3(bestset[i], bestset[j], bestset[k])) ok = 0;
    printf("N=%d f=%d check=%s set=", N, best, ok ? "ok" : "BAD");
    for (int i = best - 1; i >= 0; i--) printf("%d%s", bestset[i], i ? "," : "\n");
    fflush(stdout);
  }
  return 0;
}
