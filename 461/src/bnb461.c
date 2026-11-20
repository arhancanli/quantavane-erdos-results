/* Exact min over n of f(n,t) for Erdos #461 (program 1, C).
   f depends on the residues r_p mod p^{e_p} (p < t prime, p^{e_p} >= t minimal) only through the "pattern"
   v_p(j) = max{a <= e_p : j = r_p mod p^a}, j = 1..t. We enumerate all distinct patterns per prime, then DFS over
   primes (small first) keeping, for each position, the partial value as an exact (p, exponent) signature encoded
   as an exact class id: positions are compared by refinement of a partition, so no hashing is involved. Lower bound = number of classes so far (classes only
   split when more primes are added). Reflection j -> t+1-j is broken by requiring the pattern of p = 2 to be
   <= its mirror in a fixed order. Usage: bnb461 t [initial_upper_bound]  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXT 64
int t, np, P[32], E[32];
int npat[32]; unsigned char (*pat[32])[MAXT+1];
long long nodes = 0; int best; int bestchoice[32], choice[32];
static int cls[32][MAXT+1]; /* class id per position after processing primes 0..i-1 */
static int refine(int depth, const unsigned char *v, int *out){
  /* new class = pair (old class, v) -> renumber */
  static int map[ (MAXT+1) * 8 ];
  int ncls = 0; memset(map, -1, sizeof(map));
  for (int j = 1; j <= t; j++){ int key = cls[depth][j] * 8 + v[j]; if (map[key] < 0) map[key] = ncls++; out[j] = map[key]; }
  return ncls; }
void dfs(int i, int ncls){
  nodes++;
  if (ncls >= best) return;
  if (i == np){ best = ncls; memcpy(bestchoice, choice, sizeof(int)*np); return; }
  for (int k = 0; k < npat[i]; k++){
    choice[i] = k; int c = refine(i, pat[i][k], cls[i+1]);
    if (c < best) dfs(i + 1, c);
  }
}
int main(int argc, char **argv){
  t = atoi(argv[1]); if (t < 2 || t > MAXT){ fprintf(stderr, "t must be in [2,%d]\n", MAXT); return 1; }
  int ub = argc > 2 ? atoi(argv[2]) : -1; best = ub >= 0 ? ub + 1 : t + 1;
  for (int q = 2; q < t; q++){ int pr = 1; for (int d = 2; d*d <= q; d++) if (q % d == 0) pr = 0; if (pr){ P[np] = q; long long x = 1; int e = 0; while (x < t){ x *= q; e++; } E[np] = e; np++; } }
  for (int i = 0; i < np; i++){
    long long mod = 1; for (int a = 0; a < E[i]; a++) mod *= P[i];
    pat[i] = malloc(sizeof(*pat[i]) * (mod + 1)); npat[i] = 0;
    for (long long r = 0; r < mod; r++){
      unsigned char v[MAXT+1]; v[0] = 0;
      for (int j = 1; j <= t; j++){ int a = 0; long long pa = 1; while (a < E[i]){ pa *= P[i]; if (((j - r) % pa + pa) % pa == 0) a++; else break; } v[j] = a; }
      int dup = 0; for (int k = 0; k < npat[i] && !dup; k++) if (!memcmp(pat[i][k], v, t + 1)) dup = 1;
      if (!dup){ memcpy(pat[i][npat[i]], v, t + 1); npat[i]++; }
    }
  }
  /* symmetry: keep only patterns of p=2 that are lexicographically <= their mirror */
  { int w = 0; for (int k = 0; k < npat[0]; k++){ unsigned char m[MAXT+1]; m[0]=0; for (int j = 1; j <= t; j++) m[j] = pat[0][k][t+1-j];
      if (memcmp(pat[0][k], m, t + 1) <= 0){ memcpy(pat[0][w], pat[0][k], t + 1); w++; } } npat[0] = w; }
  for (int j = 0; j <= t; j++) cls[0][j] = 0;
  dfs(0, 1);
  if (ub >= 0 && best == ub + 1){ printf("t=%d no configuration with f <= %d (min_f > %d) nodes=%lld\n", t, ub, ub, nodes); return 0; }
  printf("t=%d min_f=%d nodes=%lld patterns:", t, best, nodes); for (int i = 0; i < np; i++) printf(" %d:%d", P[i], npat[i]);
  printf("\nargmin exponents per prime (positions 1..t):\n");
  for (int i = 0; i < np; i++){ printf("p=%d:", P[i]); for (int j = 1; j <= t; j++) printf("%d", pat[i][bestchoice[i]][j]); printf("\n"); }
  return 0; }
