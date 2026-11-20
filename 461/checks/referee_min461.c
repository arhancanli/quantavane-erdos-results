/* Referee program for Erdos #461 small-t minima (written independently of bnb461*.c / dfs461.py).

   Method: PAIRWISE collision masks, not exponent patterns.
   Referee lemma (R): for positive m < m' with delta = m' - m and k = v_p(delta),
       v_p(m) == v_p(m')  <=>  p^(k+1) does not divide m  AND  p^(k+1) does not divide m'.
   Hence s_t(n+i) == s_t(n+j) (i < j, j - i < t) iff for EVERY prime p < t neither n+i nor n+j is divisible
   by p^(v_p(j-i)+1). Since j - i < t <= p^(e_p), k + 1 <= e_p, so the test only needs x_p = n mod p^(e_p).
   No cap enters: the relation computed for the full prime set is exactly equality of s_t from the definition.

   For a subset S of primes the same test restricted to S is equality of (v_p)_{p in S}: an equivalence relation.
   Number of classes = #{j : no i < j is equivalent to j}; it can only grow when primes are added (prune).
   alive[j] = bitmask of i < j still equivalent to j. Choosing x_p kills pair (i,j) if p^(k+1) | x_p+i or x_p+j.

   Search: DFS over primes (order selectable: ascending or DESCENDING), branching on residues x_p mod p^(e_p),
   with residues merged only when their kill tables are bit-identical (exact). No symmetry reduction.
   Optional one-step lookahead bound (lemma L): final count >= max over unprocessed primes q of
   min over x_q of the class count after adding q alone to the current set.

   Usage: referee_min461 t [order a|d|r<seed>] [init_best] [lookahead 0|1] [variant]
     order: a = ascending primes, d = descending, r<seed> = 2,3 first then a seeded random order of the rest,
            w = 3,2,5,7,... ascending, v = ascending for p <= t/2 then the primes p > t/2 in descending order.
     init_best: search for counts < init_best (default t+1).  variant: 0 = correct;
     1 = RED: every cap lowered to e_p - 1 (pairs with v_p(delta) >= e_p - 1 never split by p);
     2 = RED: primes p <= t instead of p < t;  3 = RED: kill test checks only the larger position j;
     4 = RED: off-by-one window of t+1 numbers (n..n+t), primes < t;  5 = RED: every cap set to 1 (prime support only). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
static int t, tprime, np, P[40], E[40], CAP[40], order_desc = 0, lookahead = 0, variant = 0;
static long long Q[40];
static int npat[40]; static u64 *K[40]; static long long *REP[40];
static u64 alive[42][64];
static int best, found = 0, choice[40], bestchoice[40];
static long long nodes = 0;

static int vp(long long d, int p){ int k = 0; while (d % p == 0){ d /= p; k++; } return k; }
static long long ipow(long long b, int e){ long long r = 1; while (e-- > 0) r *= b; return r; }

static void build(void){
  int lim = (variant == 2) ? tprime : tprime - 1;   /* primes below tprime; t = number of positions */
  int tmpP[40], tn = 0;
  for (int q = 2; q <= lim; q++){ int pr = 1; for (int d = 2; d * d <= q; d++) if (q % d == 0){ pr = 0; break; } if (pr) tmpP[tn++] = q; }
  np = tn;
  for (int i = 0; i < np; i++) P[i] = (order_desc == 1) ? tmpP[np - 1 - i] : tmpP[i];
  if (order_desc == -1 && np >= 2){ int tmp = P[0]; P[0] = P[1]; P[1] = tmp; }      /* order w: 3,2,5,7,... */
  if (order_desc == -2){                              /* order v: ascending for p <= t/2, then descending */
    int h = 0; while (h < np && 2 * P[h] <= t) h++;
    for (int a = h, b = np - 1; a < b; a++, b--){ int tmp = P[a]; P[a] = P[b]; P[b] = tmp; }
  }
  if (order_desc >= 2){                               /* random order: seed = order_desc; primes 2,3 kept first */
    unsigned long long st = (unsigned long long)order_desc * 6364136223846793005ULL + 1442695040888963407ULL;
    for (int i = np - 1; i > 2; i--){
      st = st * 6364136223846793005ULL + 1442695040888963407ULL;
      int j = 2 + (int)((st >> 33) % (unsigned long long)(i - 1));
      int tmp = P[i]; P[i] = P[j]; P[j] = tmp;
    }
  }
  for (int i = 0; i < np; i++){
    int p = P[i], e = 0; long long x = 1; while (x < t){ x *= p; e++; }
    E[i] = e; Q[i] = x; CAP[i] = (variant == 1) ? e - 1 : (variant == 5) ? 1 : e;
    K[i] = malloc(sizeof(u64) * t * Q[i]); REP[i] = malloc(sizeof(long long) * Q[i]); npat[i] = 0;
    u64 cur[64];
    for (long long r = 0; r < Q[i]; r++){            /* r = n mod p^e */
      for (int j = 0; j < t; j++){                    /* position j+1 */
        u64 m = 0;
        for (int a = 0; a < j; a++){                  /* earlier position a+1 */
          int k = vp((long long)(j - a), p);
          if (k >= CAP[i]) continue;                  /* only reachable in RED variant 1 (k < e_p always) */
          long long pk = ipow(p, k + 1);
          int hitj = ((r + j + 1) % pk) == 0, hita = ((r + a + 1) % pk) == 0;
          if (variant == 3) hita = 0;
          if (hitj || hita) m |= (u64)1 << a;
        }
        cur[j] = m;
      }
      int dup = 0;
      for (int k2 = 0; k2 < npat[i] && !dup; k2++) if (!memcmp(K[i] + (size_t)k2 * t, cur, sizeof(u64) * t)) dup = 1;
      if (!dup){ memcpy(K[i] + (size_t)npat[i] * t, cur, sizeof(u64) * t); REP[i][npat[i]] = r; npat[i]++; }
    }
  }
}

static int count_after(const u64 *al, const u64 *k){ int c = 0; for (int j = 0; j < t; j++) c += ((al[j] & ~k[j]) == 0); return c; }

static void dfs(int i, int cnt){
  nodes++;
  if (cnt >= best) return;
  if (i == np){ best = cnt; found = 1; memcpy(bestchoice, choice, sizeof(int) * np); return; }
  if (lookahead && i + 1 < np){
    for (int q = i + 1; q < np; q++){
      int mn = 1 << 30;
      for (int k = 0; k < npat[q] && mn >= best; k++){ int c = count_after(alive[i], K[q] + (size_t)k * t); if (c < mn) mn = c; }
      if (mn >= best) return;
    }
  }
  for (int k = 0; k < npat[i]; k++){
    const u64 *kk = K[i] + (size_t)k * t; int c = 0;
    for (int j = 0; j < t; j++){ u64 a = alive[i][j] & ~kk[j]; alive[i + 1][j] = a; c += (a == 0); }
    if (c < best){ choice[i] = k; dfs(i + 1, c); }
  }
}

int main(int argc, char **argv){
  if (argc < 2){ fprintf(stderr, "usage\n"); return 1; }
  t = atoi(argv[1]);
  if (argc > 2) order_desc = (argv[2][0] == 'd') ? 1 : (argv[2][0] == 'r') ? 2 + atoi(argv[2] + 1)
                           : (argv[2][0] == 'w') ? -1 : (argv[2][0] == 'v') ? -2 : 0;
  best = (argc > 3) ? atoi(argv[3]) : t + 1;
  int init = best;
  if (argc > 4) lookahead = atoi(argv[4]);
  if (argc > 5) variant = atoi(argv[5]);
  tprime = t;
  if (variant == 4) t = t + 1;                        /* RED: window n..n+t (t+1 numbers), primes still < tprime */
  if (t < 1 || t > 64){ fprintf(stderr, "t out of range\n"); return 1; }
  build();
  for (int j = 0; j < t; j++) alive[0][j] = (j == 0) ? 0 : (((u64)1 << j) - 1);
  dfs(0, 1);
  printf("t=%d order=%s lookahead=%d variant=%d init_best=%d nodes=%lld found=%d min_f=%s%d\n", t,
         order_desc == 1 ? "desc" : order_desc >= 2 ? "random" : order_desc == -1 ? "w(3,2,5..)" :
         order_desc == -2 ? "v(asc to t/2, then desc)" : "asc", lookahead, variant, init, nodes, found, found ? "" : ">=", best);
  printf("prime order:"); for (int i = 0; i < np; i++) printf(" %d", P[i]); printf("\n");
  if (found){
    printf("witness n mod p^e:");
    for (int i = 0; i < np; i++) printf(" %d^%d:%lld", P[i], E[i], REP[i][bestchoice[i]]);
    printf("\n");
  }
  printf("distinct residue classes per prime:"); for (int i = 0; i < np; i++) printf(" %d:%d", P[i], npat[i]); printf("\n");
  return 0;
}
