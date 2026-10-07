// Adversary best response (exact) against a fixed deterministic prover RULE, discrete game.
// Order O* (unanchored): lines 015 024 036 123 146 256 345. Patterns = bitmask of steps joined.
// Returns max over adversary plays of max_j cost_j.
#include <vector>
#include <map>
#include <unordered_map>
#include <functional>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <algorithm>
using namespace std;
int lineMask[7]; int M, C, H0, H1;
typedef vector<pair<int,int>> State; // (pattern, count)
struct Key { int j; State s; bool operator==(const Key&o) const {return j==o.j && s==o.s;} };
struct KH { size_t operator()(const Key&k) const { size_t h=k.j*1000003u; for(auto&p:k.s){h=h*1315423911u+p.first*131+p.second;} return h; } };
unordered_map<Key,int,KH> memo;
bool unsafe(int S){ for(int l=0;l<7;l++) if((lineMask[l]&S)==lineMask[l]) return true; return false; }
bool forcedAt(int p,int j){ return unsafe(p|(1<<j)); }
// can pattern p ever become forced at some future step >= j (given it may join any subset of steps >= j)?
bool alive(int p,int j){ // exists future step s>=j and future set F subset of [j,s) such that p|F|{s} unsafe while p|F safe
  // simple: alive iff exists line L with |L \ p| >= 1 and L\p subset of [j,7)
  for(int l=0;l<7;l++){ int rest=lineMask[l]&~p; if(rest==0) continue; bool ok=true; for(int s=0;s<7;s++) if((rest>>s)&1) if(s<j) ok=false; if(ok) return true; } return false; }
// threatening at step j: not forced, and p|{j} creates a new 'dangerous pair' (some line L with j in L, |L\(p|{j})|==1 and the missing step > j)
bool threatening(int p,int j){ if(forcedAt(p,j)) return false; int q=p|(1<<j);
  for(int l=0;l<7;l++){ if(!((lineMask[l]>>j)&1)) continue; int rest=lineMask[l]&~q; if(__builtin_popcount(rest)==1){ int s=__builtin_ctz(rest); if(s>j && !( (lineMask[l]&~p) ==  (1<<s) )) return true; } }
  return false; }
bool has(int p,int s){ return (p>>s)&1; }
// prover rule: returns avoid counts per state entry
vector<int> rule(int j, const State& st, int& cost){
  int n=st.size(); vector<int> a(n,0); cost=0;
  for(int i=0;i<n;i++) if(forcedAt(st[i].first,j)){ a[i]=st[i].second; cost+=a[i]; }
  int budget=C-cost; if(budget<0) budget=0;
  auto avoidClass=[&](function<bool(int)> pred, int maxAvoid){ // avoid up to maxAvoid from class (threatening only)
    int done=0; for(int i=0;i<n && done<maxAvoid && budget>0;i++){ int p=st[i].first; if(a[i]<st[i].second && threatening(p,j) && pred(p)){ int x=min({st[i].second-a[i], maxAvoid-done, budget}); a[i]+=x; done+=x; budget-=x; cost+=x; } } };
  auto countClass=[&](function<bool(int)> pred){ int c=0; for(int i=0;i<n;i++) if(threatening(st[i].first,j) && pred(st[i].first)) c+=st[i].second-a[i]; return c; };
  if(j==1){ avoidClass([](int p){return has(p,0);}, 1<<30); }
  else if(j==2){ int c0=countClass([](int p){return has(p,0);}); avoidClass([](int p){return has(p,0);}, max(0,c0-H0));
                 int c1=countClass([](int p){return has(p,1)&&!has(p,0);}); avoidClass([](int p){return has(p,1)&&!has(p,0);}, max(0,c1-H1)); }
  else if(j==3){ avoidClass([](int p){return has(p,0)&&!has(p,2);}, 1<<30); avoidClass([](int p){return has(p,0);}, 1<<30); }
  else if(j==4){ avoidClass([](int p){return has(p,3)&&(has(p,0)||has(p,1));}, 1<<30);
                 avoidClass([](int p){return has(p,1)&&!has(p,2)&&!has(p,3);}, 1<<30);
                 avoidClass([](int p){return has(p,3)&&!has(p,2);}, 1<<30);
                 avoidClass([](int p){return true;}, 1<<30); }
  else if(j==5){ // avoid G2 vertices not already in K=(0&3)|(1&4)
                 avoidClass([](int p){return has(p,2)&&!((has(p,0)&&has(p,3))||(has(p,1)&&has(p,4)));}, 1<<30);
                 avoidClass([](int p){return true;}, 1<<30); }
  return a; }
int solve(int j, const State& st){
  if(j==7) return 0; Key key{j,st}; auto it=memo.find(key); if(it!=memo.end()) return it->second;
  int cost; vector<int> a=rule(j,st,cost); int n=st.size();
  int best=cost; vector<int> r(n,0);
  function<void(int,int)> rec=[&](int k,int used){ if(k==n){ map<int,int> mp; for(int q=0;q<n;q++){ int p=st[q].first; int stay=st[q].second-r[q]; if(stay>0 && alive(p,j+1)) mp[p]+=stay; if(r[q]>0){ int np=p|(1<<j); if(alive(np,j+1)) mp[np]+=r[q]; } } int fr=M-used; if(fr>0 && alive(1<<j,j+1)) mp[1<<j]+=fr; int v=solve(j+1,State(mp.begin(),mp.end())); if(v>best) best=v; return; }
    int p=st[k].first; int mx=0; if(!forcedAt(p,j) && threatening(p,j)) mx=min(st[k].second-a[k], M-used);
    for(int x=0;x<=mx;x++){ r[k]=x; rec(k+1,used+x);} r[k]=0; };
  rec(0,0); memo[key]=best; return best; }
int main(int argc,char**argv){ const char* L[7]={"015","024","036","123","146","256","345"}; for(int l=0;l<7;l++){ int mk=0; for(const char*c=L[l];*c;c++) mk|=1<<(*c-'0'); lineMask[l]=mk; }
  M=atoi(argv[1]); C=atoi(argv[2]); H0=atoi(argv[3]); H1=atoi(argv[4]);
  printf("m=%d C=%d H0=%d H1=%d -> adversary max cost %d (states %zu)\n",M,C,H0,H1,solve(0,State()),memo.size()); }
