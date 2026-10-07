#include "lib72.h"

int NN, NP;
int pidx[MAXN][MAXN];
int px[512], py[512];

void lib_init(int n){
  NN = n; NP = 0;
  for (int x = 0; x < n; x++) for (int y = x+1; y < n; y++){ pidx[x][y] = pidx[y][x] = NP; px[NP]=x; py[NP]=y; NP++; }
}

void pairs_of_block(mask b, pset *out){
  memset(out, 0, sizeof(pset));
  for (int x = 0; x < NN; x++) if (b >> x & 1)
    for (int y = x+1; y < NN; y++) if (b >> y & 1){ int p = pidx[x][y]; out->w[p>>6] |= 1ULL << (p & 63); }
}

void fam_init(fam *H){ H->m = 0; H->cap = 16; H->e = malloc(sizeof(mask)*H->cap); }
void fam_free(fam *H){ free(H->e); H->e = NULL; H->m = H->cap = 0; }
static int cmpm(const void *a, const void *b){ mask x = *(const mask*)a, y = *(const mask*)b; return x<y?-1:x>y?1:0; }
void fam_sort(fam *H){
  qsort(H->e, H->m, sizeof(mask), cmpm);
  int w = 0; for (int i = 0; i < H->m; i++) if (w == 0 || H->e[w-1] != H->e[i]) H->e[w++] = H->e[i];
  H->m = w;
}
int fam_has(const fam *H, mask E){
  int lo = 0, hi = H->m - 1;
  while (lo <= hi){ int mid = (lo+hi)/2; if (H->e[mid] == E) return 1; if (H->e[mid] < E) lo = mid+1; else hi = mid-1; }
  return 0;
}
void fam_add(fam *H, mask E){
  if (H->m == H->cap){ H->cap *= 2; H->e = realloc(H->e, sizeof(mask)*H->cap); }
  H->e[H->m++] = E;
}
void fam_copy(fam *dst, const fam *src){
  dst->m = src->m; dst->cap = src->cap > 16 ? src->cap : 16; dst->e = malloc(sizeof(mask)*dst->cap);
  memcpy(dst->e, src->e, sizeof(mask)*src->m);
}

/* ---------- bad tuple DFS ---------- */
typedef struct {
  int m; const mask *e;
  pset *cov;          /* per edge: pairs covered by its block */
  int **plist; int *pcnt;  /* per pair: edges whose block covers it */
  int maxcov;
  int maxd;
  mask *out; int found;
  int chosen[8];
  long long nodes, nodelimit;
} srch;

static int pcount(const pset *s){ int c = 0; for (int i = 0; i < PW; i++) c += __builtin_popcountll(s->w[i]); return c; }

static char *EXCL = NULL; static int EXCLcap = 0;
static int dfs(srch *S, pset cur, int d){
  S->nodes++;
  /* uncovered pairs; pick the one with the fewest NON-EXCLUDED candidates (dynamic) */
  int unc = 0; int best = -1, bc = 1<<30;
  int r = S->maxd - d;
  for (int wi = 0; wi < PW; wi++){
    int lo = wi*64; if (lo >= NP) break;
    int hi = NP - lo; if (hi > 64) hi = 64;
    uint64_t full = (hi == 64) ? ~0ULL : ((1ULL<<hi)-1);
    uint64_t u = full & ~cur.w[wi];
    while (u){ int b = __builtin_ctzll(u); u &= u-1; int p = lo + b; unc++;
      if (S->pcnt[p] < bc || (r > 0 && bc > 0)){
        int c = 0; for (int t = 0; t < S->pcnt[p]; t++) if (!EXCL[S->plist[p][t]]) c++;
        if (c < bc){ bc = c; best = p; } } }
  }
  if (unc == 0){ S->found = d; for (int i = 0; i < d; i++) S->out[i] = S->e[S->chosen[i]]; return 1; }
  if (r == 0) return 0;
  if (bc == 0) return 0;
  if (unc > r * S->maxcov) return 0;
  { int top[8] = {0};
    for (int j = 0; j < S->m; j++){ if (EXCL[j]) continue; int c = 0; for (int wi = 0; wi < PW; wi++) c += __builtin_popcountll(S->cov[j].w[wi] & ~cur.w[wi]);
      if (c > top[r-1]){ int q = r-1; while (q > 0 && top[q-1] < c){ top[q] = top[q-1]; q--; } top[q] = c; } }
    int sum = 0; for (int q = 0; q < r; q++) sum += top[q];
    if (sum < unc) return 0; }
  int *cand = malloc(sizeof(int) * S->pcnt[best]); int nc = 0;
  for (int t = 0; t < S->pcnt[best]; t++){ int j = S->plist[best][t]; if (!EXCL[j]) cand[nc++] = j; }
  int res = 0;
  for (int t = 0; t < nc && !res; t++){
    int j = cand[t];
    pset nx; for (int i = 0; i < PW; i++) nx.w[i] = cur.w[i] | S->cov[j].w[i];
    S->chosen[d] = j;
    if (dfs(S, nx, d+1)) res = 1;
    EXCL[j] = 1;               /* later siblings (and their subtrees) need not use j */
  }
  for (int t = 0; t < nc; t++) EXCL[cand[t]] = 0;
  free(cand);
  return res;
}
static void excl_ensure(int m){ if (m > EXCLcap){ EXCL = realloc(EXCL, m); EXCLcap = m; } memset(EXCL, 0, m); }

static void srch_build(srch *S, const fam *H){
  S->m = H->m; S->e = H->e;
  S->cov = malloc(sizeof(pset) * (H->m ? H->m : 1));
  S->pcnt = calloc(NP, sizeof(int));
  S->plist = malloc(sizeof(int*) * NP);
  mask full = (NN == 32) ? 0xFFFFFFFFu : ((1u<<NN)-1);
  S->maxcov = 0;
  for (int j = 0; j < H->m; j++){ pairs_of_block(full & ~H->e[j], &S->cov[j]);
    int c = pcount(&S->cov[j]); if (c > S->maxcov) S->maxcov = c;
    for (int p = 0; p < NP; p++) if (S->cov[j].w[p>>6] >> (p&63) & 1) S->pcnt[p]++; }
  for (int p = 0; p < NP; p++){ S->plist[p] = malloc(sizeof(int) * (S->pcnt[p] ? S->pcnt[p] : 1)); S->pcnt[p] = 0; }
  for (int j = 0; j < H->m; j++) for (int p = 0; p < NP; p++) if (S->cov[j].w[p>>6] >> (p&63) & 1) S->plist[p][S->pcnt[p]++] = j;
}
static void srch_free(srch *S){ for (int p = 0; p < NP; p++) free(S->plist[p]); free(S->plist); free(S->pcnt); free(S->cov); }

int find_bad(const fam *H, int maxedges, mask *out){
  srch S; srch_build(&S, H); S.maxd = maxedges; S.out = out; S.found = 0; S.nodes = 0;
  pset z; memset(&z, 0, sizeof z);
  excl_ensure(S.m > 0 ? S.m : 1);
  int r = dfs(&S, z, 0);
  int f = r ? S.found : 0;
  srch_free(&S);
  return f;
}

/* addability with explicit invalidation: caller must call addable_reset() after modifying H */
static srch CS; static int CSvalid = 0;
int addable(const fam *H, mask F, mask *cert, int *ncert){
  if (!CSvalid){ srch_build(&CS, H); CSvalid = 1; }
  mask full = (NN == 32) ? 0xFFFFFFFFu : ((1u<<NN)-1);
  pset c0; pairs_of_block(full & ~F, &c0);
  mask tmp[8];
  CS.maxd = 6; CS.out = tmp; CS.found = 0;
  excl_ensure(CS.m > 0 ? CS.m : 1);
  int r = dfs(&CS, c0, 0);
  if (r){ if (cert){ for (int i = 0; i < CS.found; i++) cert[i] = tmp[i]; *ncert = CS.found; } return 0; }
  return 1;
}
void addable_reset(void){ if (CSvalid) srch_free(&CS); CSvalid = 0; }
/* one-shot: is H minus edge 'skip' plus F (7,2)?  (assumes H\{skip} is (7,2)) */
int addable_without(const fam *H, mask skip, mask F){
  fam G; fam_init(&G); for (int t = 0; t < H->m; t++) if (H->e[t] != skip) fam_add(&G, H->e[t]);
  srch S; srch_build(&S, &G);
  mask full = (NN == 32) ? 0xFFFFFFFFu : ((1u<<NN)-1);
  pset c0; pairs_of_block(full & ~F, &c0); mask tmp[8];
  S.maxd = 6; S.out = tmp; S.found = 0;
  excl_ensure(S.m > 0 ? S.m : 1);
  int r = dfs(&S, c0, 0);
  srch_free(&S); fam_free(&G);
  return !r;
}

/* ---------- tau ---------- */
static int tbest; static const fam *TH;
static void tdfs(mask T, int sz){
  if (sz >= tbest) return;
  /* find uncovered edge; lower bound by greedy disjoint uncovered edges */
  int first = -1; mask used = T; int lb = 0;
  for (int j = 0; j < TH->m; j++){ mask E = TH->e[j]; if (E & T) continue; if (first < 0) first = j; if (!(E & used)){ used |= E; lb++; } }
  if (first < 0){ tbest = sz; return; }
  if (sz + lb >= tbest) return;
  /* branch on the uncovered edge with fewest ... just smallest popcount among first few */
  int bj = first; int bp = popc(TH->e[first]);
  for (int j = first; j < TH->m; j++){ mask E = TH->e[j]; if (E & T) continue; int pc = popc(E); if (pc < bp){ bp = pc; bj = j; } }
  mask E = TH->e[bj];
  mask excl = 0;
  while (E){ int v = __builtin_ctz(E); E &= E-1;
    tdfs(T | (1u<<v), sz+1);
    (void)excl;
  }
}
int tau_of(const fam *H){ TH = H; tbest = NN + 1; tdfs(0, 0); return tbest; }

/* ---------- twins ---------- */
mask swap_ij(mask E, int i, int j){
  int a = E >> i & 1, b = E >> j & 1;
  if (a == b) return E;
  return E ^ (1u<<i) ^ (1u<<j);
}
int is_twin(const fam *H, int i, int j){
  for (int t = 0; t < H->m; t++){ mask E = H->e[t]; if (((E>>i)&1) != ((E>>j)&1)) if (!fam_has(H, swap_ij(E,i,j))) return 0; }
  return 1;
}
int twin_classes(const fam *H, int *cls){
  int nc = 0; for (int v = 0; v < NN; v++) cls[v] = -1;
  for (int v = 0; v < NN; v++){ if (cls[v] >= 0) continue; cls[v] = nc;
    for (int w = v+1; w < NN; w++) if (cls[w] < 0 && is_twin(H, v, w)) cls[w] = nc;
    nc++; }
  return nc;
}
mask shift_edge(mask E, int i, int j){ if ((E>>j & 1) && !(E>>i & 1)) return E ^ (1u<<i) ^ (1u<<j); return E; }

static uint64_t rs = 88172645463325252ULL;
uint64_t rng_next(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
void rng_seed(uint64_t s){ rs = s * 2654435761ULL + 88172645463325252ULL; for (int i = 0; i < 10; i++) rng_next(); }
