// Principal-variation / strategy printer for the discrete protrusion game.
#include <vector>
#include <map>
#include <unordered_map>
#include <functional>
#include <string>
#include <sstream>
#include <cstdio>
#include <cstdlib>
#include <climits>
#include <algorithm>
using namespace std;
int NL = 7; int lineMask[7]; int budget[7]; int M;
typedef vector<pair<int,int>> State;
struct Key { int j; State s; bool operator==(const Key&o) const {return j==o.j && s==o.s;} };
struct KH { size_t operator()(const Key&k) const { size_t h=k.j*1000003u; for(auto&p:k.s){h=h*1315423911u+p.first*131+p.second;} return h; } };
unordered_map<Key,int,KH> memo;
bool deadType(int T, int j){ int fut=0; for(int s=j;s<7;s++) fut|=1<<s; for(int l=0;l<NL;l++) if((T>>l)&1) if((lineMask[l]&fut)==0) return true; return false; }
void addType(map<int,int>& mp, int T, int c, int jn){ if(c<=0) return; if(deadType(T,jn)) return; mp[T]+=c; }
struct Info { vector<int> T,C,forced,relevant,newT; int freshT; };
Info info(int j, const State& st){ Info I; int n=st.size(); I.T.resize(n); I.C.resize(n); I.forced.resize(n); I.relevant.resize(n); I.newT.resize(n);
  for(int i=0;i<n;i++){ I.T[i]=st[i].first; I.C[i]=st[i].second; int thr=0,all=1; for(int l=0;l<NL;l++) if((I.T[i]>>l)&1){ if((lineMask[l]>>j)&1) thr=1; else all=0; }
    I.relevant[i]=thr; I.forced[i]=all; int nt=0; for(int l=0;l<NL;l++) if(((I.T[i]>>l)&1)&&!((lineMask[l]>>j)&1)) nt|=1<<l; I.newT[i]=nt; }
  I.freshT=0; for(int l=0;l<NL;l++) if(!((lineMask[l]>>j)&1)) I.freshT|=1<<l; return I; }
State nextState(int j, const Info&I, const vector<int>& r, int m){ map<int,int> mp; int used=0; for(size_t q=0;q<I.T.size();q++){ addType(mp,I.T[q],I.C[q]-r[q],j+1); addType(mp,I.newT[q],r[q],j+1); used+=r[q]; } addType(mp,I.freshT,m-used,j+1); return State(mp.begin(),mp.end()); }
int solve(int j, const State& st);
// enumerate adversary replies
void advReplies(int j, const Info& I, const vector<int>& a, int m, function<void(const vector<int>&)> f){
  int n=I.T.size(); vector<int> r(n,0);
  function<void(int,int)> rec=[&](int k,int used){ if(k==n){ f(r); return; } int mx=(I.relevant[k]&&!I.forced[k])?min(I.C[k]-a[k],m-used):0; for(int x=0;x<=mx;x++){ r[k]=x; rec(k+1,used+x);} r[k]=0; }; rec(0,0); }
void proverMoves(const Info& I, function<void(const vector<int>&,int)> f){ int n=I.T.size(); vector<int> a(n,0);
  function<void(int,int)> rec=[&](int i,int cost){ if(i==n){ f(a,cost); return; } if(I.forced[i]){ a[i]=I.C[i]; rec(i+1,cost+I.C[i]); a[i]=0; return;} if(!I.relevant[i]){ rec(i+1,cost); return;} for(int x=0;x<=I.C[i];x++){ a[i]=x; rec(i+1,cost+x);} a[i]=0; }; rec(0,0); }
int solve(int j, const State& st){
  if(j==7) return 0; Key key{j,st}; auto it=memo.find(key); if(it!=memo.end()) return it->second;
  int m=budget[j]*M; Info I=info(j,st);
  if(m==0){ map<int,int> mp; for(size_t i=0;i<I.T.size();i++) addType(mp,I.T[i],I.C[i],j+1); int v=solve(j+1,State(mp.begin(),mp.end())); memo[key]=v; return v; }
  int best=INT_MAX;
  proverMoves(I,[&](const vector<int>&a,int cost){ if(cost>=best) return; int worst=cost; advReplies(j,I,a,m,[&](const vector<int>&r){ if(worst>=best) return; int v=solve(j+1,nextState(j,I,r,m)); if(v>worst) worst=v; }); if(worst<best) best=worst; });
  memo[key]=best; return best; }
string lname(int l){ string s; for(int t=0;t<7;t++) if((lineMask[l]>>t)&1) s+=char('0'+t); return s; }
string tname(int T){ string s="{"; bool f=true; for(int l=0;l<NL;l++) if((T>>l)&1){ if(!f) s+=","; s+=lname(l); f=false;} return s+"}"; }
string sname(const State& st){ string s; for(auto&p:st){ s+=tname(p.first)+":"+to_string(p.second)+" "; } return s; }
// print principal variation: prover best move; adversary best reply (first maximizing)
void printPV(int j, State st, int depth, string ind){
  while(j<7 && budget[j]==0){ map<int,int> mp; Info I=info(j,st); for(size_t i=0;i<I.T.size();i++) addType(mp,I.T[i],I.C[i],j+1); st=State(mp.begin(),mp.end()); j++; }
  if(j==7||depth==0) return; int m=budget[j]*M; Info I=info(j,st); int v=solve(j,st);
  printf("%sstep %d value %d state: %s\n",ind.c_str(),j,v,sname(st).c_str());
  // list all prover moves achieving v
  vector<pair<vector<int>,int>> good;
  proverMoves(I,[&](const vector<int>&a,int cost){ if(cost>v) return; int worst=cost; advReplies(j,I,a,m,[&](const vector<int>&r){ int w=solve(j+1,nextState(j,I,r,m)); if(w>worst) worst=w; }); if(worst==v) good.push_back({a,cost}); });
  for(size_t g=0; g<good.size() && g<(size_t)atoi(getenv("NGOOD")?getenv("NGOOD"):"1"); g++){
    auto& a=good[g].first; string as; for(size_t i=0;i<a.size();i++) if(a[i]) as+=tname(I.T[i])+":"+to_string(a[i])+" ";
    printf("%s  prover avoids [%s] cost %d\n",ind.c_str(),as.c_str(),good[g].second);
    // adversary replies achieving value v (those that are 'best')
    int bw=-1; vector<vector<int>> br; advReplies(j,I,a,m,[&](const vector<int>&r){ int w=solve(j+1,nextState(j,I,r,m)); if(w>bw){bw=w; br.clear();} if(w==bw) br.push_back(r); });
    for(size_t b=0;b<br.size() && b<(size_t)atoi(getenv("NREP")?getenv("NREP"):"1");b++){ string rs; for(size_t i=0;i<br[b].size();i++) if(br[b][i]) rs+=tname(I.T[i])+":"+to_string(br[b][i])+" ";
      printf("%s    adversary reuses [%s] -> %d\n",ind.c_str(),rs.c_str(),bw);
      printPV(j+1,nextState(j,I,br[b],m),depth-1,ind+"      "); }
  }
}
int main(int argc,char**argv){ string ls=argv[1]; stringstream ss(ls); string w; int li=0; while(ss>>w){ int mk=0; for(char c:w) mk|=1<<(c-'0'); lineMask[li++]=mk; }
  string b=argv[2]; for(int i=0;i<7;i++) budget[i]=b[i]-'0'; M=atoi(argv[3]); int depth=atoi(argv[4]);
  printf("value %d\n", solve(0,State()));
  printf("lines: "); for(int l=0;l<7;l++) printf("L%d=%s ",l,lname(l).c_str()); printf("\n");
  printPV(0,State(),depth,""); }
