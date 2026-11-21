/* Referee's naive brute force (own code): every subset of the points of a small plane, as a bitmask.
 * Input as for exh.c (forced points ignored). Prints, for each C from 1 to K, the number of subsets
 * S with 1 <= |S cap l| <= C for all lines, and the least such C. N_points <= 40. */
#include <stdio.h>
#include <stdint.h>
int main(void) {
    int NP, NL, K; if (scanf("%d %d %d", &NP, &NL, &K) != 3 || NP > 40) return 2;
    uint64_t L[64];
    for (int l = 0; l < NL; l++) { L[l] = 0; for (int j = 0; j < K; j++) { int p; if (scanf("%d", &p) != 1) return 2; L[l] |= (uint64_t)1 << p; } }
    long long count[32] = {0};
    uint64_t total = (uint64_t)1 << NP;
    for (uint64_t S = 1; S < total; S++) {
        int mx = 0, ok = 1;
        for (int l = 0; l < NL; l++) {
            int c = __builtin_popcountll(S & L[l]);
            if (c == 0) { ok = 0; break; }
            if (c > mx) mx = c;
        }
        if (ok) count[mx]++;
    }
    long long cum = 0; int least = -1;
    for (int C = 1; C <= K; C++) { cum += count[C]; printf("C=%d sets_with_max_load_exactly_C %lld cumulative(1..C) %lld\n", C, count[C], cum); if (cum > 0 && least < 0) least = C; }
    printf("least C = %d\n", least);
    return 0;
}
