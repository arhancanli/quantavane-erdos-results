/* Program B for Erdos #311 (written separately from program A).
   delta(N) = min over A subset {1..N} of |1 - sum 1/a|, excluding 0.
   Partition: Q = even numbers 2,4,...,2q (q = min(floor(N/2), 26)); P = all other numbers in 1..N.
   P = P_hi u P_lo with |P_lo| = c <= 25. Sums over L = lcm(1..N) as signed 128-bit.
   Q sums sorted ascending; P_lo sums sorted ascending; for every subset of P_hi a two-pointer sweep
   (P_lo ascending, target L - s descending, pointer into Q moving down). Reports the minimum, its
   number of attaining (P subset, neighbour) events, and the best numerator before reduction.
   Usage: delta_merge_b N */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef __int128 i128;
static i128 g128(i128 a, i128 b){ if (a < 0) a = -a; if (b < 0) b = -b; while (b) { i128 t = a % b; a = b; b = t; } return a; }
static void put(i128 x){ char b[64]; int k = 0; if (x == 0) { printf("0"); return; } if (x < 0) { putchar('-'); x = -x; } while (x) { b[k++] = '0' + (int)(x % 10); x /= 10; } while (k) putchar(b[--k]); }
static int cmp(const void *a, const void *b){ i128 x = *(const i128 *)a, y = *(const i128 *)b; return (x > y) - (x < y); }
static i128 *subset_sums(const i128 *w, int k){ i128 *s = malloc(sizeof(i128) << k); if (!s) { fprintf(stderr, "oom\n"); exit(1); } s[0] = 0;
  for (int i = 0; i < k; i++) { size_t half = (size_t)1 << i; for (size_t j = 0; j < half; j++) s[half + j] = s[j] + w[i]; } return s; }
int main(int argc, char **argv){
  int N = atoi(argv[1]);
  i128 L = 1; for (int a = 2; a <= N; a++) L = L / g128(L, a) * a;
  int q = N / 2; if (q > 26) q = 26;
  int inQ[200] = {0}; i128 wq[64]; for (int i = 0; i < q; i++) { inQ[2 * (i + 1)] = 1; wq[i] = L / (2 * (i + 1)); }
  i128 wp[64]; int pe[64]; int h = 0; for (int a = 1; a <= N; a++) if (!inQ[a]) { pe[h] = a; wp[h] = L / a; h++; }
  int c = h < 25 ? h : 25; int hh = h - c;   /* P_lo = first c of P, P_hi = rest */
  i128 *Y = subset_sums(wq, q); size_t nq = (size_t)1 << q; qsort(Y, nq, sizeof(i128), cmp);
  i128 *X = subset_sums(wp, c); size_t nx = (size_t)1 << c; qsort(X, nx, sizeof(i128), cmp);
  i128 best = -1; unsigned long long events = 0;
  for (uint64_t hm = 0; hm < (1ull << hh); hm++) {
    i128 s = 0; for (int i = 0; i < hh; i++) if ((hm >> i) & 1) s += wp[c + i];
    size_t j = nq;   /* invariant: Y[j..] >= target, Y[..j-1] < target */
    for (size_t i = 0; i < nx; i++) {
      i128 T = L - s - X[i];
      while (j > 0 && Y[j - 1] >= T) j--;
      /* candidates: the largest Y < T (index j-1) and the smallest Y > T (first index >= j with Y > T) */
      if (j > 0) { i128 d = T - Y[j - 1]; if (best < 0 || d < best) { best = d; events = 1; } else if (d == best) events++; }
      size_t k = j; while (k < nq && Y[k] == T) k++;
      if (k < nq) { i128 d = Y[k] - T; if (best < 0 || d < best) { best = d; events = 1; } else if (d == best) events++; }
    }
  }
  i128 gg = g128(best, L);
  printf("N=%d delta=", N); put(best / gg); putchar('/'); put(L / gg); printf(" events=%llu\n", events);
  return 0;
}
