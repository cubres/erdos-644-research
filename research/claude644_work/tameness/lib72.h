/* lib72.h -- exact small-case tools for (7,2) families (N <= 32 points, edges as uint32 masks).
   Bad tuple <=> <= 7 edges whose complement blocks cover every pair {x,y}, x<y (N>=2; points then covered too).
   All searches are exact DFS (no heuristics affect correctness). */
#ifndef LIB72_H
#define LIB72_H
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 32
#define PW 8               /* 8*64 = 512 >= 496 pairs */
typedef uint32_t mask;
typedef struct { uint64_t w[PW]; } pset;

extern int NN, NP;                 /* points, pairs */
extern int pidx[MAXN][MAXN];
extern int px[512], py[512];
void lib_init(int n);

static inline int popc(mask m){ return __builtin_popcount(m); }
void pairs_of_block(mask b, pset *out);   /* pairs inside b */

typedef struct {
  int m;           /* number of edges */
  mask *e;         /* edges, sorted ascending */
  int cap;
} fam;

void fam_init(fam *H);
void fam_free(fam *H);
void fam_sort(fam *H);           /* sort + dedupe */
int  fam_has(const fam *H, mask E);
void fam_add(fam *H, mask E);    /* append (call fam_sort after batch) */
void fam_copy(fam *dst, const fam *src);

/* find a bad subfamily of <= 7 edges among H; returns count found (0 if (7,2)); idx filled with edges */
int find_bad(const fam *H, int maxedges, mask *out);
/* is H u {F} (7,2)?  Assumes H is (7,2).  Returns 1 if addable.  If not, fills cert (<=6 edges) */
int addable(const fam *H, mask F, mask *cert, int *ncert);
/* is there a bad tuple of H u X that uses at least one edge of X (X small list)? generic: check all of H u X */
int tau_of(const fam *H);
int twin_classes(const fam *H, int *cls);  /* returns number of classes; cls[v] = class id */
mask shift_edge(mask E, int i, int j);     /* replace j by i if j in E, i notin E */
mask swap_ij(mask E, int i, int j);
int is_twin(const fam *H, int i, int j);
void addable_reset(void);
int addable_without(const fam *H, mask skip, mask F);
uint64_t rng_next(void);
void rng_seed(uint64_t s);
#endif
