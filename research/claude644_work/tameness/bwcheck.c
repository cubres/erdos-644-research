/* bwcheck.c -- exact test of LEMMA BW (bounded shifting width => type-closed block core with small tau loss).
   H (7,2) k-uniform.  Shifting preorder: i >= j iff E in H, j in E, i notin E => E-j+i in H.
   Minimum chain cover (Dilworth) of the strict order (class order + index order inside twin classes).
   For block length L: each chain cut into consecutive blocks of L positions from the top.
   H_grid := union of full block-profile classes contained in H.  CLAIM: tau(H_grid) >= tau(H) - 2 w L.
   usage: bwcheck N k seed trials mode   (mode 0 random greedy saturated, 1 random (7,2) partial,
                                          2 = partial then full conditional-shift compression (small width)) */
#include "lib72.h"
static mask *allk; static int nall;
static void shuffle(mask *a, int n){ for (int i = n-1; i > 0; i--){ int j = rng_next() % (i+1); mask t = a[i]; a[i] = a[j]; a[j] = t; } }
static void grow(fam *H, int stop){
  mask *ord = malloc(sizeof(mask)*nall); memcpy(ord, allk, sizeof(mask)*nall); shuffle(ord, nall); addable_reset();
  for (int t = 0; t < nall; t++){ if (stop > 0 && H->m >= stop) break; if (fam_has(H, ord[t])) continue;
    if (addable(H, ord[t], NULL, NULL)){ fam_add(H, ord[t]); fam_sort(H); addable_reset(); } }
  addable_reset(); free(ord); }
static void condcompress(fam *H){
  int again = 1;
  while (again){ again = 0;
    for (int j = 1; j < NN; j++) for (int i = 0; i < j; i++) for (int t = 0; t < H->m; t++){
      mask E = H->e[t]; if (!(E>>j&1) || (E>>i&1)) continue; mask F = E ^ (1u<<i) ^ (1u<<j);
      if (fam_has(H, F) || !addable_without(H, E, F)) continue;
      H->e[t] = F; fam_sort(H); again = 1; t = -1; } } }
static int geq(const fam *H, int i, int j){
  for (int t = 0; t < H->m; t++){ mask E = H->e[t]; if ((E>>j&1) && !(E>>i&1)) if (!fam_has(H, E ^ (1u<<i) ^ (1u<<j))) return 0; }
  return 1; }
static int gt[MAXN][MAXN], matchR[MAXN], matchL[MAXN], vis[MAXN];
static int aug(int u){ for (int v = 0; v < NN; v++) if (gt[u][v] && !vis[v]){ vis[v] = 1; if (matchR[v] < 0 || aug(matchR[v])){ matchR[v] = u; matchL[u] = v; return 1; } } return 0; }

int main(int argc, char **argv){
  int n = atoi(argv[1]), k = atoi(argv[2]); rng_seed(atoll(argv[3])); int trials = atoi(argv[4]), mode = atoi(argv[5]);
  lib_init(n); allk = malloc(sizeof(mask)*1000000); nall = 0; for (mask s = 0; s < (1u<<n); s++) if (popc(s) == k) allk[nall++] = s;
  long checks = 0, viol = 0, corechecks = 0, coreviol = 0;
  for (int tr = 0; tr < trials; tr++){
    fam H; fam_init(&H);
    if (mode == 0) grow(&H, 0); else { grow(&H, 1 + rng_next() % (nall/3+1)); if (mode == 2) condcompress(&H); }
    int t0 = tau_of(&H);
    int ge[MAXN][MAXN]; for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) ge[i][j] = (i == j) || geq(&H, i, j);
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) gt[i][j] = (i != j) && ge[i][j] && (!ge[j][i] || i < j);
    for (int v = 0; v < n; v++){ matchR[v] = -1; matchL[v] = -1; }
    int mm = 0; for (int u = 0; u < n; u++){ memset(vis, 0, sizeof vis); if (aug(u)) mm++; }
    int w = n - mm;
    /* chains: start at points with no predecessor (matchR == -1), follow matchL */
    int chain[MAXN], pos[MAXN], nc = 0;
    for (int v = 0; v < n; v++) if (matchR[v] < 0){ int x = v, p = 0; while (x >= 0){ chain[x] = nc; pos[x] = p++; x = matchL[x]; } nc++; }
    /* sanity: consecutive chain elements comparable in >= (transitive closure is automatic for a preorder) */
    for (int x = 0; x < n; x++) for (int y = 0; y < n; y++) if (chain[x] == chain[y] && pos[x] < pos[y] && !ge[x][y]) printf("BUG chain order\n");
    printf("trial %d: m=%d tau=%d width=%d\n", tr, H.m, t0, w);
    for (int L = 1; L <= n; L++){
      /* block id of each point */
      int blk[MAXN], nb = 0; int base[MAXN]; for (int c = 0; c < nc; c++){ base[c] = nb; int len = 0; for (int x = 0; x < n; x++) if (chain[x] == c) len++; nb += (len + L - 1) / L; }
      for (int x = 0; x < n; x++) blk[x] = base[chain[x]] + pos[x] / L;
      /* profile classes: key = counts per block (4 bits each, nb <= 16) */
      if (nb > 16) continue;
      /* map key -> (inH count, total) using simple open hashing */
      int HS = 1 << 16; uint64_t *key = calloc(HS, 8); int *tot = calloc(HS, 4), *inh = calloc(HS, 4); char *used = calloc(HS, 1);
      uint64_t *kk = malloc(8 * nall);
      for (int t = 0; t < nall; t++){ uint64_t K = 0; mask E = allk[t]; while (E){ int x = __builtin_ctz(E); E &= E-1; K += 1ULL << (4*blk[x]); }
        kk[t] = K; uint64_t h = (K * 0x9E3779B97F4A7C15ULL) >> 48; while (used[h] && key[h] != K) h = (h+1) & (HS-1);
        used[h] = 1; key[h] = K; tot[h]++; if (fam_has(&H, allk[t])) inh[h]++; }
      /* CORE STEP: every edge E missing all top blocks => whole class of e-up (profile pushed up one block per chain) in H */
      { int topblk[MAXN*2] = {0}; for (int c = 0; c < nc; c++) topblk[base[c]] = 1;
        int nxt[64]; for (int b = 0; b < nb; b++) nxt[b] = -1;
        for (int c = 0; c < nc; c++){ int len = 0; for (int x = 0; x < n; x++) if (chain[x] == c) len++; int q = (len + L - 1)/L; for (int r = 1; r < q; r++) nxt[base[c]+r] = base[c]+r-1; }
        for (int t = 0; t < H.m; t++){ mask E = H.e[t]; int bad = 0; int cnt[64] = {0};
          mask EE = E; while (EE){ int x = __builtin_ctz(EE); EE &= EE-1; if (topblk[blk[x]]) bad = 1; cnt[blk[x]]++; }
          if (bad) continue;
          uint64_t K = 0; for (int b = 0; b < nb; b++) if (cnt[b]) K += (uint64_t)cnt[b] << (4*nxt[b]);
          uint64_t h = (K * 0x9E3779B97F4A7C15ULL) >> 48; int found = 0; while (used[h]){ if (key[h] == K){ found = 1; break; } h = (h+1) & (HS-1); }
          corechecks++;
          if (!found || inh[h] != tot[h]){ coreviol++; printf("   CORE VIOLATION L=%d edge %u\n", L, E); } } }
      fam G; fam_init(&G);
      for (int t = 0; t < nall; t++){ uint64_t K = kk[t]; uint64_t h = (K * 0x9E3779B97F4A7C15ULL) >> 48; while (key[h] != K) h = (h+1) & (HS-1);
        if (inh[h] == tot[h]) fam_add(&G, allk[t]); }
      fam_sort(&G);
      int tg = G.m ? tau_of(&G) : 0;
      checks++; int ok = tg >= t0 - 2*w*L; if (!ok) viol++;
      if (0) printf("   L=%d blocks=%d |H_grid|=%d tau(H_grid)=%d  bound tau-2wL=%d %s\n", L, nb, G.m, tg, t0 - 2*w*L, ok ? "" : "VIOLATION");
      fam_free(&G); free(key); free(tot); free(inh); free(used); free(kk);
    }
    fam_free(&H);
  }
  printf("SUMMARY n=%d k=%d mode=%d: checks %ld violations %ld | core-step checks %ld violations %ld\n", n, k, mode, checks, viol, corechecks, coreviol);
  return 0;
}
