/* ops.c -- test candidate compressions on random (7,2) k-uniform families (exact).
   usage: ops N k seed trials mode   (mode 0: random greedy SATURATED; mode 1: random (7,2) partial, stop at random size)
   For every family H and ordered pair (i,j):
     op1 standard shift S_ij(H)            op2 union shift H u S_ij(H)
     op3 symmetrization H u sigma_ij(H)    op4 Zykov clone (j := copy of i)
     op5 conditional shift (move E -> E-j+i only if (7,2) survives; repeat to stability)
   Reports, per op: #applications that changed H, #that broke (7,2), tau drops; prints first counterexample. */
#include "lib72.h"

static mask *allk; static int nall;
static void gen_all(int n, int k){
  nall = 0; allk = malloc(sizeof(mask) * 1000000);
  for (mask m = 0; m < (1u<<n); m++) if (popc(m) == k) allk[nall++] = m;
}
static void shuffle(mask *a, int n){ for (int i = n-1; i > 0; i--){ int j = rng_next() % (i+1); mask t = a[i]; a[i] = a[j]; a[j] = t; } }

static void random_72(fam *H, int stopsize){
  fam_init(H);
  mask *ord = malloc(sizeof(mask)*nall); memcpy(ord, allk, sizeof(mask)*nall); shuffle(ord, nall);
  addable_reset();
  for (int t = 0; t < nall; t++){
    if (stopsize > 0 && H->m >= stopsize) break;
    if (addable(H, ord[t], NULL, NULL)){ fam_add(H, ord[t]); fam_sort(H); addable_reset(); }
  }
  addable_reset(); free(ord);
}
static void print_fam(const char *tag, const fam *H){
  printf("%s m=%d :", tag, H->m);
  for (int t = 0; t < H->m; t++){ printf(" "); for (int v = 0; v < NN; v++) if (H->e[t]>>v&1) printf("%c", v<10?'0'+v:'a'+v-10); }
  printf("\n");
}
static int is72(const fam *H){ mask o[8]; return find_bad(H, 7, o) == 0; }

int main(int argc, char **argv){
  int n = atoi(argv[1]), k = atoi(argv[2]); uint64_t seed = atoll(argv[3]); int trials = atoi(argv[4]); int mode = atoi(argv[5]);
  lib_init(n); rng_seed(seed); gen_all(n, k);
  long chg[6] = {0}, brk[6] = {0}, drop[6][4] = {{0}}; int shown[6] = {0};
  long twinhist[MAXN+1] = {0}; long tauhist[MAXN+1] = {0};
  for (int tr = 0; tr < trials; tr++){
    fam H; int stop = mode == 1 ? 1 + rng_next() % (nall/3 + 1) : 0;
    random_72(&H, stop);
    int t0 = tau_of(&H); int cls[MAXN]; int nc = twin_classes(&H, cls);
    twinhist[nc]++; tauhist[t0]++;
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++){ if (i == j) continue;
      for (int op = 1; op <= 5; op++){
        fam G; fam_init(&G); int changed = 0;
        if (op == 1){ for (int t = 0; t < H.m; t++){ mask E = H.e[t], F = shift_edge(E, i, j); if (F != E && !fam_has(&H, F)){ fam_add(&G, F); changed = 1; } else fam_add(&G, E); } }
        if (op == 2){ for (int t = 0; t < H.m; t++){ mask E = H.e[t], F = shift_edge(E, i, j); fam_add(&G, E); if (F != E && !fam_has(&H, F)){ fam_add(&G, F); changed = 1; } } }
        if (op == 3){ for (int t = 0; t < H.m; t++){ mask E = H.e[t], F = swap_ij(E, i, j); fam_add(&G, E); if (F != E && !fam_has(&H, F)){ fam_add(&G, F); changed = 1; } } }
        if (op == 4){ for (int t = 0; t < H.m; t++){ mask E = H.e[t]; int a = E>>i&1, b = E>>j&1;
            if (b && !a){ if (!fam_has(&H, swap_ij(E,i,j))) changed = 1; continue; }
            fam_add(&G, E); if (a && !b){ mask F = swap_ij(E,i,j); fam_add(&G, F); if (!fam_has(&H, F)) changed = 1; } } }
        if (op == 5){ fam_copy(&G, &H); int again = 1;
          while (again){ again = 0;
            for (int t = 0; t < G.m; t++){ mask E = G.e[t], F = shift_edge(E, i, j);
              if (F == E || fam_has(&G, F)) continue;
              if (addable_without(&G, E, F)){ G.e[t] = F; fam_sort(&G); changed = 1; again = 1; break; } } } }
        fam_sort(&G);
        if (changed){ chg[op]++;
          int ok = is72(&G); int t1 = tau_of(&G);
          if (!ok){ brk[op]++; if (shown[op] < 1){ shown[op]++; printf("op%d BREAKS (7,2): n=%d k=%d pair i=%d j=%d tau %d\n", op, n, k, i, j, t0); print_fam("  H", &H); print_fam("  G", &G); } }
          int d = t0 - t1; if (d < 0) d = -1; if (d > 2) d = 2; drop[op][d+1]++;
        }
        fam_free(&G);
      }
    }
    fam_free(&H);
  }
  printf("SUMMARY n=%d k=%d mode=%d trials=%d\n", n, k, mode, trials);
  const char *nm[6] = {"", "shift", "unionshift", "symm", "zykov", "condshift"};
  for (int op = 1; op <= 5; op++) printf("  %-10s changed %ld  broke72 %ld  tau: up %ld same %ld drop1 %ld drop>=2 %ld\n", nm[op], chg[op], brk[op], drop[op][0], drop[op][1], drop[op][2], drop[op][3]);
  printf("  twin-class histogram:"); for (int c = 1; c <= n; c++) if (twinhist[c]) printf(" %d:%ld", c, twinhist[c]); printf("\n");
  printf("  tau histogram:"); for (int c = 0; c <= n; c++) if (tauhist[c]) printf(" %d:%ld", c, tauhist[c]); printf("\n");
  return 0;
}
