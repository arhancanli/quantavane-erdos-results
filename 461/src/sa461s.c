/* Exploratory search for Erdos #461: minimise f(n,t) = #distinct t-smooth parts of n+1..n+t.
   f depends only on r_p = (-n) mod p^{e_p} for primes p < t (p^{e_p} >= t minimal): v_p(n+j) truncated
   = max a <= e_p with j = r_p mod p^a. Values compared by a random 64-bit additive hash (exploration only;
   best configurations are re-checked exactly by a separate Python program). Usage: sa461 t iters seed */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint64_t rs = 88172645463325252ULL;
static uint64_t rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int t, np, P[2000], E[2000]; long long PE[2000][24]; long long R[2000];
uint64_t H[2000][24]; uint64_t hv[4096]; int vpos[2000][4096];
int vp_at(int i, int j){ int a = 0; while (a < E[i] && ((j - R[i]) % PE[i][a+1] + PE[i][a+1]) % PE[i][a+1] == 0) a++; return a; }
int cmpu(const void*a,const void*b){ uint64_t x=*(uint64_t*)a,y=*(uint64_t*)b; return x<y?-1:x>y; }
int count_distinct(void){ static uint64_t s[4096]; memcpy(s, hv+1, t*sizeof(uint64_t)); qsort(s,t,8,cmpu); int c=1; for(int i=1;i<t;i++) if(s[i]!=s[i-1]) c++; return c; }
void set_r(int i, long long r){
  for (int j = 1; j <= t; j++) { int a = vpos[i][j]; if (a) hv[j] -= H[i][a]; }
  R[i] = r;
  for (int j = 1; j <= t; j++) { int a = vp_at(i, j); vpos[i][j] = a; if (a) hv[j] += H[i][a]; }
}
int main(int argc, char**argv){
  t = atoi(argv[1]); long iters = atol(argv[2]); rs ^= (uint64_t)atol(argv[3]) * 0x9E3779B97F4A7C15ULL;
  for (int q = 2; q < t; q++){ int pr = 1; for (int d = 2; d*d <= q; d++) if (q % d == 0) pr = 0; if (!pr) continue;
    P[np] = q; long long x = 1; int e = 0; PE[np][0] = 1; while (x < t){ x *= q; e++; PE[np][e] = x; } E[np] = e;
    for (int a = 0; a <= e; a++) H[np][a] = rnd(); np++; }
  memset(hv, 0, sizeof hv); memset(vpos, 0, sizeof vpos);
  long long seedr[2000]; for (int i = 0; i < np; i++) seedr[i] = -1;
  if (argc > 4){ FILE *fp = fopen(argv[4], "r"); int pp; long long rr; while (fp && fscanf(fp, " %d:%lld", &pp, &rr) == 2){ for (int i = 0; i < np; i++) if (P[i] == pp) seedr[i] = rr; } if (fp) fclose(fp); }
  for (int i = 0; i < np; i++) set_r(i, seedr[i] >= 0 ? seedr[i] % PE[i][E[i]] : (long long)(rnd() % PE[i][E[i]]));
  int cur = count_distinct(), best = cur; double T0 = argc > 5 ? atof(argv[5]) : 2.0;
  long long bestR[2000]; memcpy(bestR, R, sizeof(long long)*np);
  for (long it = 0; it < iters; it++){
    double T = T0 * (1.0 - (double)it/iters) + 0.02;
    int i = rnd() % np; long long old = R[i]; long long nr;
    if (rnd() % 3 == 0) nr = (old + (long long)(rnd() % P[i]) * (PE[i][E[i]] / P[i])) % PE[i][E[i]]; else nr = rnd() % PE[i][E[i]];
    set_r(i, nr); int nf = count_distinct();
    if (nf <= cur || (double)(rnd() % 1000000) / 1e6 < __builtin_exp((cur - nf) / T)) { cur = nf; if (cur < best){ best = cur; memcpy(bestR, R, sizeof(long long)*np);} }
    else set_r(i, old);
  }
  printf("t=%d best=%d ratio=%.4f residues:", t, best, (double)best/t);
  for (int i = 0; i < np; i++) printf(" %d:%lld", P[i], bestR[i]); printf("\n");
  return 0;
}
