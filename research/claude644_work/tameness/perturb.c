/* perturb.c -- start from K_X^{(k)} (X = first n0 points) inside N points, delete d random edges of K_X,
   re-saturate in random order; report tau, twin-class size profile, number of points in classes of size < L.
   usage: perturb N k n0 d trials seed */
#include "lib72.h"
static int geq(const fam *H, int i, int j){ for (int t = 0; t < H->m; t++){ mask E = H->e[t]; if ((E>>j&1) && !(E>>i&1)) if (!fam_has(H, E ^ (1u<<i) ^ (1u<<j))) return 0; } return 1; }
static int gt[MAXN][MAXN], mR[MAXN], vis[MAXN];
static int aug(int u){ for (int v = 0; v < NN; v++) if (gt[u][v] && !vis[v]){ vis[v] = 1; if (mR[v] < 0 || aug(mR[v])){ mR[v] = u; return 1; } } return 0; }
static int width_of(const fam *H){ int ge[MAXN][MAXN]; for (int i = 0; i < NN; i++) for (int j = 0; j < NN; j++) ge[i][j] = (i==j) || geq(H,i,j);
  for (int i = 0; i < NN; i++) for (int j = 0; j < NN; j++) gt[i][j] = (i != j) && ge[i][j] && (!ge[j][i] || i < j);
  for (int v = 0; v < NN; v++) mR[v] = -1; int mm = 0; for (int u = 0; u < NN; u++){ memset(vis,0,sizeof vis); if (aug(u)) mm++; } return NN - mm; }
static void shuffle(mask *a, int n){ for (int i = n-1; i > 0; i--){ int j = rng_next() % (i+1); mask t = a[i]; a[i] = a[j]; a[j] = t; } }
int main(int argc, char **argv){
  int n = atoi(argv[1]), k = atoi(argv[2]), n0 = atoi(argv[3]), d = atoi(argv[4]), trials = atoi(argv[5]); rng_seed(atoll(argv[6]));
  lib_init(n);
  mask *all = malloc(sizeof(mask)*1000000); int na = 0; for (mask s = 0; s < (1u<<n); s++) if (popc(s) == k) all[na++] = s;
  long hist_small[MAXN+1] = {0};
  for (int tr = 0; tr < trials; tr++){
    fam H; fam_init(&H);
    mask *kx = malloc(sizeof(mask)*na); int nk = 0; for (int t = 0; t < na; t++) if (all[t] < (1u<<n0)) kx[nk++] = all[t];
    shuffle(kx, nk); for (int t = d; t < nk; t++) fam_add(&H, kx[t]); fam_sort(&H); free(kx);
    mask *ord = malloc(sizeof(mask)*na); memcpy(ord, all, sizeof(mask)*na); shuffle(ord, na);
    addable_reset();
    for (int t = 0; t < na; t++){ if (fam_has(&H, ord[t])) continue; if (addable(&H, ord[t], NULL, NULL)){ fam_add(&H, ord[t]); fam_sort(&H); addable_reset(); } }
    addable_reset(); free(ord);
    int cls[MAXN]; int nc = twin_classes(&H, cls); int sz[MAXN] = {0}; for (int v = 0; v < n; v++) sz[cls[v]]++;
    int inX = 1; /* is X still a clique? */ for (int t = 0; t < na; t++) if (all[t] < (1u<<n0) && !fam_has(&H, all[t])) { inX = 0; break; }
    int small = 0; for (int v = 0; v < n; v++) if (sz[cls[v]] < 3) small++;
    hist_small[small]++;
    printf("trial %d: m=%d tau=%d classes=%d sizes=", tr, H.m, tau_of(&H), nc); for (int c = 0; c < nc; c++) printf("%d%s", sz[c], c+1<nc?",":""); printf("  K_X restored=%d  pts in classes<3: %d  width=%d\n", inX, small, width_of(&H));
    if (getenv("DUMPW") && tau_of(&H) >= atoi(getenv("DUMPW"))){ printf("  FAM"); for (int t = 0; t < H.m; t++) printf(" %u", H.e[t]); printf("\n"); }
    fam_free(&H);
  }
  printf("SUMMARY N=%d k=%d n0=%d d=%d: hist of #points in classes of size<3:", n, k, n0, d); for (int s = 0; s <= n; s++) if (hist_small[s]) printf(" %d:%ld", s, hist_small[s]); printf("\n");
  return 0;
}
