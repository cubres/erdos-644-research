/* satur: read "N k m e1..em"; saturate (lexicographic random order with seed) keeping (7,2); print tau, #twin classes,
   width of shifting preorder, and the saturated family */
#include "lib72.h"
int main(int argc, char **argv){
  int n, k, m; uint64_t seed = argc > 1 ? atoll(argv[1]) : 1; rng_seed(seed);
  while (scanf("%d %d %d", &n, &k, &m) == 3){
    lib_init(n); fam H; fam_init(&H);
    for (int i = 0; i < m; i++){ unsigned x; scanf("%u", &x); fam_add(&H, x); }
    fam_sort(&H);
    mask *all = malloc(sizeof(mask) * 1000000); int na = 0;
    for (mask s = 0; s < (1u<<n); s++) if (popc(s) == k) all[na++] = s;
    for (int i = na-1; i > 0; i--){ int j = rng_next() % (i+1); mask t = all[i]; all[i] = all[j]; all[j] = t; }
    addable_reset();
    for (int t = 0; t < na; t++){ if (fam_has(&H, all[t])) continue; if (addable(&H, all[t], NULL, NULL)){ fam_add(&H, all[t]); fam_sort(&H); addable_reset(); } }
    addable_reset();
    int cls[MAXN]; int nc = twin_classes(&H, cls);
    printf("SAT m=%d tau=%d classes=%d cls=", H.m, tau_of(&H), nc); for (int v = 0; v < n; v++) printf("%d", cls[v]); printf("\n");
    printf("FAM"); for (int t = 0; t < H.m; t++) printf(" %u", H.e[t]); printf("\n"); fflush(stdout);
    free(all); fam_free(&H);
  }
  return 0;
}
