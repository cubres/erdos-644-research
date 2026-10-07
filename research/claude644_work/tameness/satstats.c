/* satstats.c -- statistics of (7,2)-SATURATED k-uniform families on N points (exact).
   usage: satstats N k seed trials mode
     mode 0: random greedy saturation from empty
     mode 1: "tau-greedy": repeatedly try to add an addable k-subset of a MAXIMUM independent set (raises alpha
             pressure -> high tau); when none, finish by random greedy saturation.
   Per family: tau, #twin classes, shifting preorder i >= j (H is S_ij-stable: E in H, j in E, i notin E =>
   E-j+i in H), #comparable class pairs, width (max antichain of classes, Dilworth via matching),
   TOTAL? (width 1 => shifted up to relabelling => Lemma SH applies);
   and test B-L3: for each incomparable pair, is S_ij(H) or S_ji(H) (7,2)?
   Prints families that are extreme (max tau seen with width>1). */
#include "lib72.h"

static mask *allk; static int nall;
static void gen_all(int n, int k){ nall = 0; allk = malloc(sizeof(mask)*2000000);
  for (mask m = 0; m < (1u<<n); m++) if (popc(m) == k) allk[nall++] = m; }
static void shuffle(mask *a, int n){ for (int i = n-1; i > 0; i--){ int j = rng_next() % (i+1); mask t = a[i]; a[i] = a[j]; a[j] = t; } }
static int is72(const fam *H){ mask o[8]; return find_bad(H, 7, o) == 0; }
static void print_fam(const char *tag, const fam *H){
  printf("%s m=%d :", tag, H->m);
  for (int t = 0; t < H->m; t++){ printf(" "); for (int v = 0; v < NN; v++) if (H->e[t]>>v&1) printf("%c", v<10?'0'+v:'a'+v-10); }
  printf("\n"); }

/* independent-set indicator over all subsets (N <= 24) */
static unsigned char *indep;
static void compute_indep(const fam *H){
  mask full = 1u << NN;
  for (mask S = 0; S < full; S++) indep[S] = 1;
  for (int t = 0; t < H->m; t++) indep[H->e[t]] = 0;
  /* S dependent iff contains an edge: propagate upward */
  for (int v = 0; v < NN; v++) for (mask S = 0; S < full; S++) if ((S>>v&1) && !indep[S ^ (1u<<v)]) indep[S] = 0;
}
static void saturate_random(fam *H){
  mask *ord = malloc(sizeof(mask)*nall); memcpy(ord, allk, sizeof(mask)*nall); shuffle(ord, nall);
  addable_reset();
  for (int t = 0; t < nall; t++){ if (fam_has(H, ord[t])) continue;
    if (addable(H, ord[t], NULL, NULL)){ fam_add(H, ord[t]); fam_sort(H); addable_reset(); } }
  addable_reset(); free(ord);
}
static void saturate_taugreedy(fam *H, int k){
  for (;;){
    compute_indep(H);
    int best = 0; mask full = 1u << NN;
    for (mask S = 0; S < full; S++) if (indep[S] && popc(S) > best) best = popc(S);
    if (best < k) break;
    /* collect k-subsets of maximum independent sets, random order, add first addable */
    mask *cand = malloc(sizeof(mask)*nall); int nc = 0;
    for (int t = 0; t < nall; t++){ mask F = allk[t]; if (!indep[F] || fam_has(H, F)) continue;
      /* F inside some maximum independent set? check supersets of size best that are independent: cheap test by random extension */
      cand[nc++] = F; }
    shuffle(cand, nc);
    int added = 0; addable_reset();
    for (int t = 0; t < nc && !added; t++){
      mask F = cand[t];
      /* require F to lie in an independent set of size best */
      int inmax = 0; mask rest = (full-1) & ~F;
      /* enumerate subsets of rest of size best-k (small) */
      int need = best - popc(F);
      if (need == 0) inmax = 1; else {
        for (mask S = rest; S; S = (S-1) & rest) if (popc(S) == need && indep[F|S]){ inmax = 1; break; } }
      if (!inmax) continue;
      if (addable(H, F, NULL, NULL)){ fam_add(H, F); fam_sort(H); added = 1; }
    }
    addable_reset(); free(cand);
    if (!added) break;
  }
  saturate_random(H);
}
static int stable(const fam *H, int i, int j){ /* i >= j : S_ij-stable */
  for (int t = 0; t < H->m; t++){ mask E = H->e[t]; if ((E>>j&1) && !(E>>i&1)) if (!fam_has(H, E ^ (1u<<i) ^ (1u<<j))) return 0; }
  return 1; }
/* bipartite matching for Dilworth on classes */
static int nC, rel[MAXN][MAXN], matchR[MAXN], vis[MAXN];
static int aug(int u){ for (int v = 0; v < nC; v++) if (rel[u][v] && !vis[v]){ vis[v] = 1; if (matchR[v] < 0 || aug(matchR[v])){ matchR[v] = u; return 1; } } return 0; }

int main(int argc, char **argv){
  int n = atoi(argv[1]), k = atoi(argv[2]); uint64_t seed = atoll(argv[3]); int trials = atoi(argv[4]); int mode = atoi(argv[5]);
  lib_init(n); rng_seed(seed); gen_all(n, k); indep = malloc(1u << n);
  long totcnt = 0, bl3_pairs = 0, bl3_fail = 0; int shown = 0; int dumped = 0;
  long tab[MAXN+1][MAXN+1]; memset(tab, 0, sizeof tab); /* tau x width */
  long tabc[MAXN+1][MAXN+1]; memset(tabc, 0, sizeof tabc); /* tau x classes */
  for (int tr = 0; tr < trials; tr++){
    fam H; fam_init(&H);
    if (mode == 0) saturate_random(&H); else saturate_taugreedy(&H, k);
    int t0 = tau_of(&H); int cls[MAXN]; nC = twin_classes(&H, cls);
    int rep[MAXN]; for (int c = 0; c < nC; c++) for (int v = 0; v < n; v++) if (cls[v] == c){ rep[c] = v; break; }
    int comp = 0;
    for (int a = 0; a < nC; a++) for (int b = 0; b < nC; b++){ rel[a][b] = 0; if (a != b && stable(&H, rep[a], rep[b])) rel[a][b] = 1; }
    for (int a = 0; a < nC; a++) for (int b = a+1; b < nC; b++) if (rel[a][b] || rel[b][a]) comp++;
    for (int v = 0; v < nC; v++) matchR[v] = -1;
    int mm = 0; for (int u = 0; u < nC; u++){ memset(vis, 0, sizeof vis); if (aug(u)) mm++; }
    int width = nC - mm;
    if (width == 1) totcnt++;
    if (argc > 6 && nC >= atoi(argv[6]) && dumped < 3){ dumped++; printf("DUMP tau=%d classes=%d width=%d\n", t0, nC, width); print_fam("  H", &H); }
    tab[t0][width]++; tabc[t0][nC]++;
    /* B-L3 */
    for (int a = 0; a < nC; a++) for (int b = a+1; b < nC; b++) if (!rel[a][b] && !rel[b][a]){
      int i = rep[a], j = rep[b]; bl3_pairs++;
      int okk = 0;
      for (int dir = 0; dir < 2 && !okk; dir++){ int x = dir ? j : i, y = dir ? i : j;
        fam G; fam_init(&G);
        for (int t = 0; t < H.m; t++){ mask E = H.e[t], F = shift_edge(E, x, y); if (F != E && !fam_has(&H, F)) fam_add(&G, F); else fam_add(&G, E); }
        fam_sort(&G); if (is72(&G)) okk = 1; fam_free(&G); }
      if (!okk){ bl3_fail++; if (shown < 2){ shown++; printf("B-L3 FAILS: n=%d k=%d tau=%d classes=%d width=%d pair (%d,%d): neither shift is (7,2)\n", n, k, t0, nC, width, i, j); print_fam("  H", &H); } }
    }
    fam_free(&H);
  }
  printf("SUMMARY n=%d k=%d mode=%d trials=%d: total-preorder (shifted up to relabelling) %ld\n", n, k, mode, trials, totcnt);
  printf("  tau x width:"); for (int t = 0; t <= n; t++) for (int w = 0; w <= n; w++) if (tab[t][w]) printf(" (tau%d,w%d):%ld", t, w, tab[t][w]); printf("\n");
  printf("  tau x classes:"); for (int t = 0; t <= n; t++) for (int w = 0; w <= n; w++) if (tabc[t][w]) printf(" (tau%d,c%d):%ld", t, w, tabc[t][w]); printf("\n");
  printf("  B-L3 incomparable pairs %ld, pairs where neither shift keeps (7,2): %ld\n", bl3_pairs, bl3_fail);
  return 0;
}
