/* Referee invariant (separate session, own code) for the planes of order 9: reads a plane file in Moorhouse's
 * format (one line per row, its points as numbers 0..N-1) on stdin, and counts unordered quadrangles whose three
 * diagonal points are collinear ("Fano quadrangles"), in the plane and in its dual (lines as points). For each
 * point, the number of Fano quadrangles with it as a vertex gives a multiset; the total, min, max and number of
 * distinct values are printed. Isomorphic planes give equal outputs; a plane and its dual swap the two rows.
 * Usage: cc -O2 -o fano referee_fano.c && for f in hall9 dhall9 hughes9; do ./fano < ../planes/$f.txt; done
 * Output: Hall 362880 (points 0..16128 / lines 15360..20736), dual Hall the same with the rows swapped, Hughes 235872
 * (10368 at every point and line); PG(2,9) has none (odd characteristic). So the four planes are pairwise
 * non-isomorphic. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 200
static int N, K;
static int L[MAXN][32];
static int join[MAXN][MAXN], meet[MAXN][MAXN], on[MAXN][MAXN];

static void build(void) {
    memset(on, 0, sizeof on);
    for (int l = 0; l < N; l++) for (int j = 0; j < K; j++) on[L[l][j]][l] = 1;
    for (int l = 0; l < N; l++) for (int a = 0; a < K; a++) for (int b = 0; b < K; b++)
        if (a != b) join[L[l][a]][L[l][b]] = l;
    for (int l = 0; l < N; l++) for (int m = 0; m < N; m++) if (l != m)
        for (int j = 0; j < K; j++) if (on[L[l][j]][m]) { meet[l][m] = L[l][j]; break; }
}

static void count(const char *tag) {
    static long long per[MAXN];
    memset(per, 0, sizeof per);
    long long total = 0;
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) {
        int ab = join[a][b];
        for (int c = b + 1; c < N; c++) {
            if (on[c][ab]) continue;
            int ac = join[a][c], bc = join[b][c];
            for (int d = c + 1; d < N; d++) {
                if (on[d][ab] || on[d][ac] || on[d][bc]) continue;
                int ad = join[a][d], bd = join[b][d], cd = join[c][d];
                int x = meet[ab][cd], y = meet[ac][bd], z = meet[ad][bc];
                if (on[z][join[x][y]]) { total++; per[a]++; per[b]++; per[c]++; per[d]++; }
            }
        }
    }
    long long mn = per[0], mx = per[0];
    for (int i = 1; i < N; i++) { if (per[i] < mn) mn = per[i]; if (per[i] > mx) mx = per[i]; }
    /* number of distinct per-point values */
    long long vals[MAXN]; int nv = 0;
    for (int i = 0; i < N; i++) { int f = 0; for (int j = 0; j < nv; j++) if (vals[j] == per[i]) f = 1; if (!f) vals[nv++] = per[i]; }
    printf("%s: Fano quadrangles %lld; per-point min %lld max %lld, %d distinct values\n", tag, total, mn, mx, nv);
}

int main(void) {
    char buf[4096];
    N = 0; K = 0;
    while (fgets(buf, sizeof buf, stdin)) {
        int k = 0, off = 0, v, used;
        while (sscanf(buf + off, "%d%n", &v, &used) == 1) { if (k >= 32 || N >= MAXN) return 2; L[N][k++] = v; off += used; }
        if (k == 0) continue;
        if (K == 0) K = k;
        if (k != K) return 2;
        N++;
    }
    if (N != K * K - K + 1) return 2;
    for (int l = 0; l < N; l++) for (int j = 0; j < K; j++) if (L[l][j] < 0 || L[l][j] >= N) return 2;
    build();
    count("plane");
    /* dual: point l (old line) on new line P (old point) iff incident */
    static int D[MAXN][32];
    for (int p = 0; p < N; p++) { int k = 0; for (int l = 0; l < N; l++) if (on[p][l]) D[p][k++] = l; if (k != K) return 3; }
    memcpy(L, D, sizeof D);
    build();
    count("dual ");
    return 0;
}
