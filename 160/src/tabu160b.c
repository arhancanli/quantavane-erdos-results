/* Tabu search (incremental) for k-colourings of {1..N} with every 4-term AP receiving >= 3 colours (Erdos #160).
   Per AP: colour counts and number of distinct colours; cost = #APs with <= 2 distinct colours.
   Move = recolour one position; best non-tabu move (aspiration on new best); random tie-break.
   Usage: tabu160b k N seed maxiters [init_file]; writes sol160_k<k>_N<N>_seed<seed>.txt on success. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int k, N, c[600], nap, (*AP)[4], *apl[600], napl[600]; static uint8_t (*cnt)[16]; static uint8_t *dist;
static uint64_t rs; static inline uint64_t rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int main(int argc, char **argv){
  k = atoi(argv[1]); N = atoi(argv[2]); uint64_t seed = strtoull(argv[3], 0, 10); long maxit = atol(argv[4]);
  rs = seed * 0x9E3779B97F4A7C15ull + 11;
  AP = malloc(sizeof(int[4]) * N * N); nap = 0;
  for (int a = 1; a <= N; a++) for (int d = 1; a + 3 * d <= N; d++) { for (int t = 0; t < 4; t++) AP[nap][t] = a + t * d; nap++; }
  for (int i = 1; i <= N; i++) { apl[i] = malloc(sizeof(int) * nap); napl[i] = 0; }
  for (int a = 0; a < nap; a++) for (int t = 0; t < 4; t++) apl[AP[a][t]][napl[AP[a][t]]++] = a;
  if (argc > 5) { FILE *f = fopen(argv[5], "r"); int i = 1; while (i <= N && fscanf(f, "%d", &c[i]) == 1) i++; fclose(f); for (; i <= N; i++) c[i] = rnd() % k; }
  else for (int i = 1; i <= N; i++) c[i] = rnd() % k;
  cnt = calloc(nap, 16); dist = calloc(nap, 1);
  int cost = 0;
  for (int a = 0; a < nap; a++) { for (int t = 0; t < 4; t++) if (cnt[a][c[AP[a][t]]]++ == 0) dist[a]++; if (dist[a] <= 2) cost++; }
  int best = cost; static long tabu[600][16]; memset(tabu, 0, sizeof tabu);
  for (long it = 1; it <= maxit && cost > 0; it++) {
    int bi = -1, bc = -1, bd = 1 << 30, nt = 0;
    for (int i = 1; i <= N; i++) {
      int o = c[i];
      for (int col = 0; col < k; col++) { if (col == o) continue;
        int d = 0;
        for (int j = 0; j < napl[i]; j++) { int a = apl[i][j]; int nd = dist[a] - (cnt[a][o] == 1) + (cnt[a][col] == 0);
          d += (nd <= 2) - (dist[a] <= 2); }
        int ok = tabu[i][col] < it || cost + d < best;
        if (ok && (d < bd || (d == bd && rnd() % (++nt) == 0))) { if (d < bd) nt = 1; bd = d; bi = i; bc = col; } }
    }
    if (bi < 0) continue;
    int o = c[bi];
    for (int j = 0; j < napl[bi]; j++) { int a = apl[bi][j]; int was = dist[a] <= 2;
      if (--cnt[a][o] == 0) dist[a]--; if (cnt[a][bc]++ == 0) dist[a]++; cost += (dist[a] <= 2) - was; }
    c[bi] = bc; tabu[bi][o] = it + 4 + rnd() % 12;
    if (cost < best) best = cost;
  }
  int chk = 0; for (int a = 0; a < nap; a++) { int m = 0; for (int t = 0; t < 4; t++) m |= 1 << c[AP[a][t]]; chk += __builtin_popcount(m) <= 2; }
  printf("k=%d N=%d seed=%llu final cost=%d (recount %d) best=%d\n", k, N, (unsigned long long)seed, cost, chk, best);
  if (chk == 0) { char fn[128]; sprintf(fn, "sol160_k%d_N%d_seed%llu.txt", k, N, (unsigned long long)seed); FILE *f = fopen(fn, "w"); for (int i = 1; i <= N; i++) fprintf(f, "%d%c", c[i], i == N ? '\n' : ' '); fclose(f); printf("WROTE %s\n", fn); }
  return 0;
}
