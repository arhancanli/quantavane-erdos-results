/* Referee's exhaustive search for Erdos #1159 (20 Nov 2026, own code).
 * Decides whether a plane (given as lines = lists of point labels) has a set S with
 * 1 <= |S cap l| <= C for every line l, optionally with some points forced into S.
 *
 * Input (stdin): N_points N_lines k  then each line: k labels;  then F  then F forced labels.
 * argv[1] = C, argv[2] = mode: "point" (branch include/exclude on points in a fixed order,
 * counts ALL solutions) or "line" (pick an uncovered line with fewest free points and branch on
 * which of its free points is the first one in S; stops at the first solution).
 * Output: number of solutions (point mode) or SAT/UNSAT (line mode), plus node count.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXP 400
#define MAXL 400
#define MAXK 24

static int NP, NL, K, C;
static int lines[MAXL][MAXK];
static int ptl[MAXP][MAXK]; /* lines through each point */
static int npl[MAXP];
static int cnt[MAXL];   /* chosen points on line */
static int fre[MAXL];   /* undecided points on line */
static int state[MAXP]; /* -1 undecided, 0 out, 1 in */
static long long nodes = 0, sols = 0;
static int order[MAXP];
static int solution[MAXP], have_solution = 0;

static int can_in(int p) {
    for (int j = 0; j < npl[p]; j++) if (cnt[ptl[p][j]] >= C) return 0;
    return 1;
}
static int can_out(int p) {
    for (int j = 0; j < npl[p]; j++) { int l = ptl[p][j]; if (cnt[l] == 0 && fre[l] == 1) return 0; }
    return 1;
}
static void set_in(int p) { state[p] = 1; for (int j = 0; j < npl[p]; j++) { cnt[ptl[p][j]]++; fre[ptl[p][j]]--; } }
static void unset_in(int p) { state[p] = -1; for (int j = 0; j < npl[p]; j++) { cnt[ptl[p][j]]--; fre[ptl[p][j]]++; } }
static void set_out(int p) { state[p] = 0; for (int j = 0; j < npl[p]; j++) fre[ptl[p][j]]--; }
static void unset_out(int p) { state[p] = -1; for (int j = 0; j < npl[p]; j++) fre[ptl[p][j]]++; }

static void dfs_point(int i) {
    nodes++;
    if (i == NP) { sols++; return; }
    int p = order[i];
    if (state[p] != -1) { dfs_point(i + 1); return; }
    if (can_in(p)) { set_in(p); dfs_point(i + 1); unset_in(p); }
    if (can_out(p)) { set_out(p); dfs_point(i + 1); unset_out(p); }
}

static int dfs_line(void) {
    nodes++;
    int best = -1, bf = 1 << 30;
    for (int l = 0; l < NL; l++) {
        if (cnt[l] == 0) {
            if (fre[l] == 0) return 0;
            if (fre[l] < bf) { bf = fre[l]; best = l; }
        }
    }
    if (best < 0) { /* every line covered, caps respected: a solution */
        for (int p = 0; p < NP; p++) solution[p] = (state[p] == 1);
        have_solution = 1;
        return 1;
    }
    int l = best;
    int excl[MAXK], ne = 0, found = 0;
    for (int j = 0; j < K && !found; j++) {
        int p = lines[l][j];
        if (state[p] != -1) continue;
        if (can_in(p)) { set_in(p); found = dfs_line(); unset_in(p); }
        if (found) break;
        /* next branch: p is not in S */
        if (!can_out(p)) break;
        set_out(p); excl[ne++] = p;
    }
    while (ne > 0) unset_out(excl[--ne]);
    return found;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: exh C point|line < plane\n"); return 2; }
    C = atoi(argv[1]);
    if (scanf("%d %d %d", &NP, &NL, &K) != 3) return 2;
    if (NP > MAXP || NL > MAXL || K > MAXK) return 2;
    memset(npl, 0, sizeof npl);
    for (int l = 0; l < NL; l++) {
        for (int j = 0; j < K; j++) {
            int p; if (scanf("%d", &p) != 1) return 2;
            if (p < 0 || p >= NP) return 2;
            lines[l][j] = p; ptl[p][npl[p]++] = l;
        }
        cnt[l] = 0; fre[l] = K;
    }
    for (int p = 0; p < NP; p++) state[p] = -1;
    int F; if (scanf("%d", &F) != 1) F = 0;
    for (int f = 0; f < F; f++) {
        int p; if (scanf("%d", &p) != 1) return 2;
        if (state[p] == 1) continue;
        if (!can_in(p)) { printf("forced set violates cap: UNSAT nodes 0\n"); return 0; }
        set_in(p);
    }
    /* point order: line by line, so lines are completed early */
    int k = 0, seen[MAXP]; memset(seen, 0, sizeof seen);
    for (int l = 0; l < NL; l++) for (int j = 0; j < K; j++) { int p = lines[l][j]; if (!seen[p]) { seen[p] = 1; order[k++] = p; } }
    if (strcmp(argv[2], "point") == 0) {
        dfs_point(0);
        printf("mode point C=%d solutions %lld nodes %lld\n", C, sols, nodes);
    } else {
        int r = dfs_line();
        printf("mode line C=%d %s nodes %lld\n", C, r ? "SAT" : "UNSAT", nodes);
        if (r && have_solution) {
            printf("S:");
            for (int p = 0; p < NP; p++) if (solution[p]) printf(" %d", p);
            printf("\n");
        }
    }
    return 0;
}
