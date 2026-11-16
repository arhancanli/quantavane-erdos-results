/* Program A (streaming) for Erdos #311: delta(N) = min nonzero |1 - sum_{a in A} 1/a|, A subset {1..N}.
   Exact over L = lcm(1..N) in unsigned 128-bit. Q = {N-q+1..N} (q = min(N/2, QMAX)) stored as sorted sums;
   P = {1..N-q} streamed (Gray-code order), binary search of L - x in Q's sums, exact hits skipped.
   Prints delta as a reduced fraction, the number of (x, side) pairs attaining it, and one optimal set.
   Usage: delta_stream_a N [QMAX=26] */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
static u128 gcd128(u128 a, u128 b){ while (b) { u128 t = a % b; a = b; b = t; } return a; }
static void pr(u128 x){ char t[64]; int k = 0; if (!x) { putchar('0'); return; } while (x) { t[k++] = '0' + (int)(x % 10); x /= 10; } while (k) putchar(t[--k]); }
static int cmpu(const void *a, const void *b){ u128 x = *(const u128 *)a, y = *(const u128 *)b; return x < y ? -1 : x > y; }
int main(int argc, char **argv){
  int N = atoi(argv[1]); int QMAX = argc > 2 ? atoi(argv[2]) : 26;
  u128 L = 1; for (int a = 1; a <= N; a++) L = L / gcd128(L, a) * a;
  int q = N / 2; if (q > QMAX) q = QMAX; int h = N - q;
  uint64_t nq = 1ull << q;
  u128 *Y = malloc(sizeof(u128) * nq); if (!Y) { fprintf(stderr, "oom\n"); return 1; }
  u128 wq[64], wp[64];
  for (int i = 0; i < q; i++) wq[i] = L / (h + 1 + i);
  for (int i = 0; i < h; i++) wp[i] = L / (i + 1);
  Y[0] = 0; for (int i = 0; i < q; i++) { uint64_t b = 1ull << i; for (uint64_t j = 0; j < b; j++) Y[b + j] = Y[j] + wq[i]; }
  qsort(Y, nq, sizeof(u128), cmpu);
  u128 best = 0; int have = 0; uint64_t bxm = 0; u128 by = 0; uint64_t cnt = 0;
  u128 xs = 0; uint64_t g = 0;  /* Gray code: mask = g ^ (g >> 1) */
  uint64_t np = 1ull << h;
  for (uint64_t it = 0; it < np; it++) {
    if (it) { int bit = __builtin_ctzll(it); uint64_t m = it ^ (it >> 1); if ((m >> bit) & 1) xs += wp[bit]; else xs -= wp[bit]; g = m; }
    if (xs >= L) { /* partner 0 gives xs - L unless xs == L */
      if (xs > L) { u128 d = xs - L; if (!have || d < best) { best = d; have = 1; bxm = g; by = 0; cnt = 1; } else if (d == best) cnt++; continue; }
    }
    u128 t = L - xs;
    uint64_t lo = 0, hi = nq; while (lo < hi) { uint64_t mid = (lo + hi) >> 1; if (Y[mid] < t) lo = mid + 1; else hi = mid; }
    if (lo > 0) { u128 d = t - Y[lo - 1]; if (!have || d < best) { best = d; have = 1; bxm = g; by = Y[lo - 1]; cnt = 1; } else if (d == best) cnt++; }
    uint64_t k = lo; while (k < nq && Y[k] == t) k++;
    if (k < nq) { u128 d = Y[k] - t; if (!have || d < best) { best = d; have = 1; bxm = g; by = Y[k]; cnt = 1; } else if (d == best) cnt++; }
  }
  /* recover a Q-mask with sum by */
  uint64_t bym = 0; { u128 s = 0; for (uint64_t it = 0; it < nq; it++) { if (it) { int bit = __builtin_ctzll(it); uint64_t m = it ^ (it >> 1); if ((m >> bit) & 1) s += wq[bit]; else s -= wq[bit]; if (s == by) { bym = m; break; } } else if (by == 0) { bym = 0; break; } } }
  u128 gg = gcd128(best, L);
  printf("N=%d delta=", N); pr(best / gg); putchar('/'); pr(L / gg); printf(" hits=%llu set=", (unsigned long long)cnt);
  for (int i = 0; i < h; i++) if ((bxm >> i) & 1) printf("%d,", i + 1);
  for (int i = 0; i < q; i++) if ((bym >> i) & 1) printf("%d,", h + 1 + i);
  printf("\n");
  return 0;
}
