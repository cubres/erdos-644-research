// Exact adversary best response against the ANCHORED prover rules (best order: anchor 0, live lines 124 156 235 346).
// mode 0 (cap strategy, target C=m-floor(m/4)): step2 leave <=q of G1; step3 leave <= q-|G1&G2| of G2\G1; step4 avoid G3\F4 with budget C-|F4|;
//        step5 avoid G1\F5 with budget C-|F5|.  Reports max_j c_j.
// mode 1 (profile strategy): no preemption at steps 1-3; step4/5 use budget m. Reports the cost vector maximum per step (c4,c5,c6 max separately)
#include <vector>
#include <map>
#include <unordered_map>
#include <functional>
#include <cstdio>
#include <cstdlib>
#include <algorithm>
using namespace std;
int lineMask[7]; int M, C, Q, MODE;
typedef vector<pair<int,int>> State;
struct Key { int j; State s; bool operator==(const Key&o) const {return j==o.j && s==o.s;} };
struct KH { size_t operator()(const Key&k) const { size_t h=k.j*1000003u; for(auto&p:k.s){h=h*1315423911u+p.first*131+p.second;} return h; } };
typedef vector<int> Vec; // per-step max cost (index 0..6)
unordered_map<Key,Vec,KH> memo;
bool unsafe(int S){ for(int l=0;l<7;l++) if((lineMask[l]&S)==lineMask[l]) return true; return false; }
bool forcedAt(int p,int j){ return unsafe(p|(1<<j)); }
bool has(int p,int s){ return (p>>s)&1; }
bool alive(int p,int j){ for(int l=0;l<7;l++){ int rest=lineMask[l]&~p; if(rest==0) continue; bool ok=true; for(int s=0;s<7;s++) if((rest>>s)&1) if(s<j) ok=false; if(ok) return true; } return false; }
bool threatening(int p,int j){ if(forcedAt(p,j)) return false; int q=p|(1<<j); for(int l=0;l<7;l++){ if(!((lineMask[l]>>j)&1)) continue; int rest=lineMask[l]&~q; if(__builtin_popcount(rest)==1){ int s=__builtin_ctz(rest); if(s>j) return true; } } return false; }
vector<int> rule(int j,const State& st,int& cost){ int n=st.size(); vector<int> a(n,0); cost=0;
  for(int i=0;i<n;i++) if(forcedAt(st[i].first,j)){ a[i]=st[i].second; cost+=a[i]; }
  auto avoidDownTo=[&](function<bool(int)> pred,int keep){ int avail=0; for(int i=0;i<n;i++) if(pred(st[i].first)&&threatening(st[i].first,j)) avail+=st[i].second-a[i]; int need=max(0,avail-keep); for(int i=0;i<n&&need>0;i++) if(pred(st[i].first)&&threatening(st[i].first,j)){ int x=min(need,st[i].second-a[i]); a[i]+=x; need-=x; cost+=x; } };
  auto avoidBudget=[&](function<bool(int)> pred,int budget){ for(int i=0;i<n&&budget>0;i++) if(pred(st[i].first)&&threatening(st[i].first,j)&&a[i]<st[i].second){ int x=min(budget,st[i].second-a[i]); a[i]+=x; budget-=x; cost+=x; } };
  if(MODE==0){
    if(j==2) avoidDownTo([](int p){return has(p,1);}, Q);
    if(j==3){ int p12=0; for(int i=0;i<n;i++) if(has(st[i].first,1)&&has(st[i].first,2)) p12+=st[i].second; avoidDownTo([](int p){return has(p,2)&&!has(p,1);}, max(0,Q-p12)); }
    if(j==4) avoidBudget([](int p){return has(p,3);}, C-cost);
    if(j==5) avoidBudget([](int p){return has(p,1);}, C-cost);
  } else {
    if(j==4) avoidBudget([](int p){return has(p,3);}, M-cost);
    if(j==5) avoidBudget([](int p){return has(p,1);}, M-cost);
  }
  return a; }
Vec solve(int j,const State& st){
  if(j==7) return Vec(7,0); Key key{j,st}; auto it=memo.find(key); if(it!=memo.end()) return it->second;
  Vec best(7,0);
  if(j==0){ Vec v=solve(1,st); memo[key]=v; return v; } // anchor: no outside mass
  int cost; vector<int> a=rule(j,st,cost); int n=st.size(); best[j]=cost; vector<int> r(n,0);
  function<void(int,int)> rec=[&](int k,int used){ if(k==n){ map<int,int> mp; for(int q=0;q<n;q++){ int p=st[q].first; int stay=st[q].second-r[q]; if(stay>0&&alive(p,j+1)) mp[p]+=stay; if(r[q]>0){ int np=p|(1<<j); if(alive(np,j+1)) mp[np]+=r[q]; } } int fr=M-used; if(fr>0&&alive(1<<j,j+1)) mp[1<<j]+=fr; Vec v=solve(j+1,State(mp.begin(),mp.end())); for(int s=0;s<7;s++) best[s]=max(best[s],v[s]); return; }
    int p=st[k].first; int mx=0; if(!forcedAt(p,j)&&threatening(p,j)) mx=min(st[k].second-a[k],M-used); for(int x=0;x<=mx;x++){ r[k]=x; rec(k+1,used+x);} r[k]=0; };
  rec(0,0); memo[key]=best; return best; }
int main(int argc,char**argv){ const char* L[7]={"013","026","045","124","156","235","346"}; for(int l=0;l<7;l++){ int mk=0; for(const char*c=L[l];*c;c++) mk|=1<<(*c-'0'); lineMask[l]=mk; }
  M=atoi(argv[1]); MODE=atoi(argv[2]); Q=M/4; C=M-Q; Vec v=solve(0,State());
  printf("m=%d mode=%d: worst-case per-step costs c1..c6 = ",M,MODE); for(int s=1;s<7;s++) printf("%d ",v[s]); int mx=0; for(int s=1;s<7;s++) mx=max(mx,v[s]); printf(" max=%d (ceil(3m/4)=%d)\n",mx,M-Q); }
