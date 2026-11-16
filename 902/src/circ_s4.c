/* Exhaustive search for circulant tournaments on Z_n (n odd, n <= 127) with Schutte's property S_k (k = 4 default).
   Tournament: i -> j iff (j - i) mod n in D, where for each d in 1..(n-1)/2 exactly one of d, n-d is in D.
   Vertex v dominates S iff v -> s for all s in S. Let M = {v : v -> 0} = -D. Dominators of S = intersection of (M + s).
   By translation it suffices to check 4-sets containing 0: S = {0,a,b,c}.
   Bit i of choice word x: 1 means d=i+1 in D, 0 means n-(i+1) in D.
   Usage: circ_s4 n [k] [lo hi]   (enumerates x in [lo,hi) ; default all 2^((n-1)/2))
   Output: lines "HIT n x" for every passing D, and a summary of the best near-miss (fewest failing orbits on a full scan of sampled x). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static int n, k, h;
static u128 FULL;
static inline u128 rot(u128 m, int a){ if(a==0) return m; return ((m << a) | (m >> (n - a))) & FULL; }
int main(int argc, char **argv){
  n = atoi(argv[1]); k = argc > 2 ? atoi(argv[2]) : 4; h = (n - 1) / 2;
  if (n % 2 == 0 || n > 127 || k < 2 || k > 4) { fprintf(stderr, "bad args\n"); return 1; }
  FULL = (((u128)1) << n) - 1;
  uint64_t lo = 0, hi = ((uint64_t)1) << h;
  if (argc > 4) { lo = strtoull(argv[3], 0, 10); hi = strtoull(argv[4], 0, 10); }
  /* list of (k-1)-subsets {a<b<c} of 1..n-1 */
  int maxT = (n - 1) * (n - 2) * (n - 3) / 6 + 10;
  int (*T)[3] = malloc(sizeof(int[3]) * maxT); int nt = 0;
  if (k == 4) { for (int a = 1; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { T[nt][0]=a; T[nt][1]=b; T[nt][2]=c; nt++; } }
  else if (k == 3) { for (int a = 1; a < n; a++) for (int b = a + 1; b < n; b++) { T[nt][0]=a; T[nt][1]=b; T[nt][2]=0; nt++; } }
  else { for (int a = 1; a < n; a++) { T[nt][0]=a; T[nt][1]=0; T[nt][2]=0; nt++; } }
  uint64_t hits = 0, tested = 0;
  for (uint64_t x = lo; x < hi; x++) {
    u128 D = 0;
    for (int i = 0; i < h; i++) { int d = (x >> i & 1) ? (i + 1) : (n - i - 1); D |= ((u128)1) << d; }
    /* M = -D */
    u128 M = 0; for (int d = 1; d < n; d++) if ((D >> d) & 1) M |= ((u128)1) << (n - d);
    tested++;
    int ok = 1;
    for (int t = 0; t < nt; t++) {
      u128 r = M & rot(M, T[t][0]);
      if (k >= 3) r &= rot(M, T[t][1]);
      if (k >= 4) r &= rot(M, T[t][2]);
      if (!r) { ok = 0;
        if (t > 0) { int tmp[3]; memcpy(tmp, T[t], sizeof tmp); memmove(T[1], T[0], sizeof(int[3]) * t); memcpy(T[0], tmp, sizeof tmp); }
        break; }
    }
    if (ok) { hits++; printf("HIT n=%d k=%d x=%llu D=", n, k, (unsigned long long)x); for (int d = 1; d < n; d++) if ((D >> d) & 1) printf("%d,", d); printf("\n"); fflush(stdout); }
  }
  printf("DONE n=%d k=%d range=[%llu,%llu) tested=%llu hits=%llu\n", n, k, (unsigned long long)lo, (unsigned long long)hi, (unsigned long long)tested, (unsigned long long)hits);
  return 0;
}
