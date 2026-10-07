/* compress.c -- full conditional-shift compression toward a shifted family (exact).
   usage: compress N k seed trials mode [keep_tau]
     mode 0: start from random greedy saturated (7,2) family; mode 1: random (7,2) stopped early;
     mode 2: start from saturated family grown from K_{N'}^{(k)} on the first N' points (N' max with K (7,2)),
             padded by the remaining points (high tau).
     keep_tau=1: only moves that keep tau as well.
   Process: repeat { for i<j: for each edge E with j in E, i notin E, E-j+i notin H: move if H-E+(E-j+i) is (7,2)
            [and tau unchanged] } until no move.  Reports tau before/after, whether final is shifted,
            #unshifted triples left, #twin classes before/after. */
#include "lib72.h"

static mask *allk; static int nall;
static void gen_all(int n, int k){ nall = 0; allk = malloc(sizeof(mask)*1000000);
  for (mask m = 0; m < (1u<<n); m++) if (popc(m) == k) allk[nall++] = m; }
static void shuffle(mask *a, int n){ for (int i = n-1; i > 0; i--){ int j = rng_next() % (i+1); mask t = a[i]; a[i] = a[j]; a[j] = t; } }
static void saturate(fam *H, int stopsize){
  mask *ord = malloc(sizeof(mask)*nall); memcpy(ord, allk, sizeof(mask)*nall); shuffle(ord, nall);
  addable_reset();
  for (int t = 0; t < nall; t++){ if (stopsize > 0 && H->m >= stopsize) break;
    if (fam_has(H, ord[t])) continue;
    if (addable(H, ord[t], NULL, NULL)){ fam_add(H, ord[t]); fam_sort(H); addable_reset(); } }
  addable_reset(); free(ord);
}
static int is72(const fam *H){ mask o[8]; return find_bad(H, 7, o) == 0; }
static int unshifted(const fam *H){ int c = 0;
  for (int t = 0; t < H->m; t++) for (int j = 0; j < NN; j++) if (H->e[t]>>j&1) for (int i = 0; i < j; i++) if (!(H->e[t]>>i&1))
    if (!fam_has(H, H->e[t] ^ (1u<<i) ^ (1u<<j))) c++;
  return c; }
static void print_fam(const char *tag, const fam *H){
  printf("%s m=%d :", tag, H->m);
  for (int t = 0; t < H->m; t++){ printf(" "); for (int v = 0; v < NN; v++) if (H->e[t]>>v&1) printf("%c", v<10?'0'+v:'a'+v-10); }
  printf("\n"); }

int main(int argc, char **argv){
  int n = atoi(argv[1]), k = atoi(argv[2]); uint64_t seed = atoll(argv[3]); int trials = atoi(argv[4]); int mode = atoi(argv[5]);
  int keep = argc > 6 ? atoi(argv[6]) : 0;
  lib_init(n); rng_seed(seed); gen_all(n, k);
  int np = 0; /* largest N' <= n with K_{N'}^{(k)} (7,2) */
  if (mode == 2){ for (int q = k; q <= n; q++){ fam K; fam_init(&K); for (int t = 0; t < nall; t++) if (allk[t] < (1u<<q)) fam_add(&K, allk[t]); fam_sort(&K); if (is72(&K)) np = q; fam_free(&K); } }
  int shown = 0;
  long hist[8] = {0}; long nshift = 0;
  for (int tr = 0; tr < trials; tr++){
    fam H; fam_init(&H);
    if (mode == 2){ for (int t = 0; t < nall; t++) if (allk[t] < (1u<<np)) fam_add(&H, allk[t]); fam_sort(&H); saturate(&H, 0); }
    else saturate(&H, mode == 1 ? 1 + rng_next() % (nall/3 + 1) : 0);
    int t0 = tau_of(&H); int cls[MAXN]; int c0 = twin_classes(&H, cls); int u0 = unshifted(&H);
    int moves = 0, again = 1;
    while (again){ again = 0;
      for (int j = 1; j < n; j++) for (int i = 0; i < j; i++){
        for (int t = 0; t < H.m; t++){ mask E = H.e[t]; if (!(E>>j&1) || (E>>i&1)) continue; mask F = E ^ (1u<<i) ^ (1u<<j);
          if (fam_has(&H, F)) continue;
          if (!addable_without(&H, E, F)) continue;
          if (keep){ fam G; fam_copy(&G, &H); G.e[t] = F; fam_sort(&G); int tg = tau_of(&G); fam_free(&G); if (tg != tau_of(&H)) continue; }
          H.e[t] = F; fam_sort(&H); moves++; again = 1; t = -1; } } }
    int t1 = tau_of(&H); int c1 = twin_classes(&H, cls); int u1 = unshifted(&H);
    if (!is72(&H)) printf("BUG: not 72\n");
    int d = t0 - t1; if (d < -1) d = -1; if (d > 5) d = 5; hist[d+1]++; if (u1 == 0) nshift++;
    printf("trial %d: m=%d tau %d -> %d  twins %d -> %d  unshifted triples %d -> %d  moves %d\n", tr, H.m, t0, t1, c0, c1, u0, u1, moves);
    if (u1 > 0 && shown < 2){ shown++; print_fam("  STUCK", &H); }
    fam_free(&H);
  }
  printf("SUMMARY n=%d k=%d mode=%d keep_tau=%d trials=%d (Kclique N'=%d): final shifted %ld; tau drop hist [-1..5]:", n, k, mode, keep, trials, np, nshift);
  for (int d = 0; d < 7; d++) printf(" %ld", hist[d]); printf("\n");
  return 0;
}
