/* Program B for #902: exhaustive search over Cayley tournaments on a group G of odd order n,
   given by its multiplication table (odd n <= 67 as written: 128-bit masks, triple buffer of 50000), for Schutte's property S_k (k = 3 or 4).
   Cayley tournament: x -> y iff x^{-1} y in D, where D contains exactly one of g, g^{-1} for every g != e.
   Dominators of S are the v with v^{-1} s in D for all s in S, i.e. the intersection of s*M over s in S,
   where M = D^{-1} = {v : v -> e}. Left translations act transitively, so only S containing e are checked.
   Enumeration: Gray code over the (n-1)/2 inverse pairs; the masks a*M for all a are updated incrementally
   through the multiplication table (no rotations are used). Written separately from circ_s4.c.
   Input file: first line n, then n lines of n integers: row a gives a*g for g = 0..n-1; element 0 is e.
   Usage: cayley_sk table.txt k  -> prints every passing D (as the list of elements in D) and a summary. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
int main(int argc, char **argv){
  FILE *f = fopen(argv[1], "r"); int k = atoi(argv[2]); int n;
  if (fscanf(f, "%d", &n) != 1) return 1;
  static int mul[128][128]; for (int a = 0; a < n; a++) for (int g = 0; g < n; g++) if (fscanf(f, "%d", &mul[a][g]) != 1) return 1;
  fclose(f);
  int inv[128]; for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) if (mul[a][b] == 0) inv[a] = b;
  /* group axioms sanity: identity, inverses, associativity on all triples */
  for (int a = 0; a < n; a++) if (mul[0][a] != a || mul[a][0] != a) { fprintf(stderr, "identity fails\n"); return 1; }
  for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++) if (mul[mul[a][b]][c] != mul[a][mul[b][c]]) { fprintf(stderr, "assoc fails\n"); return 1; }
  int P[64], np = 0, seen[128] = {0}; seen[0] = 1;
  for (int g = 1; g < n; g++) if (!seen[g]) { if (inv[g] == g) { fprintf(stderr, "involution\n"); return 1; } P[np++] = g; seen[g] = seen[inv[g]] = 1; }
  /* initial code 0: for every pair i, g = P[i] is in M (so g^{-1} in D) */
  u128 AM[128];
  for (int a = 0; a < n; a++) { AM[a] = 0; for (int i = 0; i < np; i++) AM[a] |= ((u128)1) << mul[a][P[i]]; }
  int (*T)[3] = malloc(sizeof(int[3]) * 50000); int nt = 0;
  if (k == 4) { for (int a = 1; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) { T[nt][0] = a; T[nt][1] = b; T[nt][2] = c; nt++; } }
  else { for (int a = 1; a < n; a++) for (int b = a + 1; b < n; b++) { T[nt][0] = a; T[nt][1] = b; T[nt][2] = 0; nt++; } }
  uint64_t total = 1ull << np, pass = 0, code = 0;
  for (uint64_t it = 0; it < total; it++) {
    if (it) { int i = __builtin_ctzll(it); code ^= 1ull << i; int g = P[i], h = inv[g];
      for (int a = 0; a < n; a++) AM[a] ^= (((u128)1) << mul[a][g]) | (((u128)1) << mul[a][h]); }
    u128 M = AM[0]; int ok = 1;
    for (int t = 0; t < nt; t++) {
      u128 r = M & AM[T[t][0]] & AM[T[t][1]];
      if (k == 4) r &= AM[T[t][2]];
      if (!r) { ok = 0; if (t > 0) { int tmp[3]; memcpy(tmp, T[t], sizeof tmp); memmove(T[1], T[0], sizeof(int[3]) * t); memcpy(T[0], tmp, sizeof tmp); } break; }
    }
    if (ok) { pass++; if (pass <= 50) { printf("PASS D="); for (int i = 0; i < np; i++) printf("%d,", ((code >> i) & 1) ? P[i] : inv[P[i]]); printf("\n"); } }
  }
  printf("SUMMARY n=%d k=%d pairs=%d tested=%llu pass=%llu\n", n, k, np, (unsigned long long)total, (unsigned long long)pass);
  return 0;
}
