/* Referee brute force for Erdos #461 (independent of the submitted programs).
   For every n in [0, PERIODS * M_t) compute s_t(n+j), j = 1..t, by full trial division over primes p < t
   (full multiplicity, no cap, no patterns), count distinct values, report the minimum and the first n attaining it.
   M_t = prod_{p<t} p^{e_p}; PERIODS = 2 checks that the minimum over two periods equals that over one.
   Usage: referee_brute461 t [periods]   (practical for t <= 13) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64;
static int t, np, P[16];
static u64 s(u64 m){ u64 r = 1; for (int i = 0; i < np; i++){ while (m % P[i] == 0){ m /= P[i]; r *= P[i]; } } return r; }
int main(int argc, char **argv){
  t = atoi(argv[1]); int periods = argc > 2 ? atoi(argv[2]) : 1;
  u64 M = 1;
  for (int q = 2; q < t; q++){ int pr = 1; for (int d = 2; d * d <= q; d++) if (q % d == 0) pr = 0;
    if (pr){ P[np++] = q; u64 x = 1; while (x < (u64)t) x *= q; M *= x; } }
  u64 buf[64]; int best = t + 1; u64 arg = 0; u64 hist[66] = {0};
  for (int j = 1; j <= t; j++) buf[(j - 1) % t] = s((u64)j);           /* window for n = 0: values s(1..t) */
  u64 N = M * (u64)periods;
  for (u64 n = 0; n < N; n++){
    if (n > 0) buf[(n + t - 1) % t] = s(n + t);                          /* slide: drop s(n), add s(n+t) */
    int d = 0;
    for (int a = 0; a < t; a++){ int seen = 0; for (int b = 0; b < a; b++) if (buf[b] == buf[a]){ seen = 1; break; } d += !seen; }
    if (n < M) hist[d]++;
    if (d < best){ best = d; arg = n; }
  }
  printf("t=%d M_t=%llu periods=%d min_f=%d first_n=%llu  count of n in [0,M_t) with f=min: %llu\n", t, M, periods, best, arg, hist[best]);
  return 0;
}
