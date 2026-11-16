/* Program A' for #902 (written separately from cayley_sk.c): Cayley tournaments on a group of odd order n <= 127
   (multiplication table input, element 0 = identity), property S_4. For each connection set D (plain binary counter
   over the inverse pairs, pair i taken as the element with the smaller index when bit i is 0), the set
   N0 = {v : v -> 0} = {v : v^{-1} in D} is built directly; a 4-set {0, a, b, c} is dominated iff the left translates
   0*N0, a*N0, b*N0, c*N0 have a common element (v dominates s iff v^{-1}s in D iff s^{-1}v in D^{-1} iff v in s*N0).
   Translates are computed on demand from the table (no incremental updates), cached per candidate.
   Usage: cayley_direct table.txt [lo hi] -> count of passing D in the range and the first few passing D. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 W;
static int n, mul[128][128], inv[128];
int main(int argc, char **argv){
  FILE *f = fopen(argv[1], "r"); if (fscanf(f, "%d", &n) != 1) return 1;
  for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) if (fscanf(f, "%d", &mul[a][b]) != 1) return 1;
  fclose(f);
  for (int a = 0; a < n; a++) { inv[a] = -1; for (int b = 0; b < n; b++) if (mul[a][b] == 0 && mul[b][a] == 0) inv[a] = b; if (inv[a] < 0) { fprintf(stderr, "no inverse\n"); return 1; } }
  int lo_el[64], hi_el[64], np = 0;
  for (int g = 1; g < n; g++) if (g < inv[g]) { lo_el[np] = g; hi_el[np] = inv[g]; np++; } else if (g == inv[g]) { fprintf(stderr, "involution\n"); return 1; }
  uint64_t lo = 0, hi = 1ull << np; if (argc > 3) { lo = strtoull(argv[2], 0, 10); hi = strtoull(argv[3], 0, 10); }
  int (*T)[3] = malloc(sizeof(int[3]) * 400000); int nt = 0;
  for (int a = 1; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { T[nt][0] = a; T[nt][1] = b; T[nt][2] = c; nt++; }
  W tr[128]; uint64_t stamp[128]; memset(stamp, 0, sizeof stamp); uint64_t gen = 0;
  uint64_t pass = 0;
  for (uint64_t x = lo; x < hi; x++) {
    gen++;
    /* D contains lo_el[i] if bit i is 0, else hi_el[i]; N0 = D^{-1} */
    W N0 = 0; int mem[64]; int nm = 0;
    for (int i = 0; i < np; i++) { int d = ((x >> i) & 1) ? hi_el[i] : lo_el[i]; int v = inv[d]; N0 |= ((W)1) << v; mem[nm++] = v; }
    int ok = 1;
    for (int t = 0; t < nt && ok; t++) {
      W r = N0;
      for (int j = 0; j < 3; j++) { int s = T[t][j];
        if (stamp[s] != gen) { W m = 0; for (int q = 0; q < nm; q++) m |= ((W)1) << mul[s][mem[q]]; tr[s] = m; stamp[s] = gen; }
        r &= tr[s]; }
      if (!r) { ok = 0; if (t > 0) { int tmp[3]; memcpy(tmp, T[t], sizeof tmp); memmove(T[1], T[0], sizeof(int[3]) * t); memcpy(T[0], tmp, sizeof tmp); } }
    }
    if (ok) { pass++; if (pass <= 20) { printf("PASS x=%llu D=", (unsigned long long)x); for (int i = 0; i < np; i++) printf("%d,", ((x >> i) & 1) ? hi_el[i] : lo_el[i]); printf("\n"); } }
  }
  printf("SUMMARY_A n=%d pairs=%d range=[%llu,%llu) pass=%llu\n", n, np, (unsigned long long)lo, (unsigned long long)hi, (unsigned long long)pass);
  return 0;
}
