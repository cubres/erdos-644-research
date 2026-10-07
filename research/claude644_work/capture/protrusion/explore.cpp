// explore from a given state: print prover's optimal moves and, for each, the adversary's best replies (1 level), then recurse along chosen branches.
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
void advReplies(const Info& I, const vector<int>& a, int m, function<void(const vector<int>&)> f){ int n=I.T.size(); vector<int> r(n,0);
  function<void(int,int)> rec=[&](int k,int used){ if(k==n){ f(r); return; } int mx=(I.relevant[k]&&!I.forced[k])?min(I.C[k]-a[k],m-used):0; for(int x=0;x<=mx;x++){ r[k]=x; rec(k+1,used+x);} r[k]=0; }; rec(0,0); }
void proverMoves(const Info& I, function<void(const vector<int>&,int)> f){ int n=I.T.size(); vector<int> a(n,0);
  function<void(int,int)> rec=[&](int i,int cost){ if(i==n){ f(a,cost); return; } if(I.forced[i]){ a[i]=I.C[i]; rec(i+1,cost+I.C[i]); a[i]=0; return;} if(!I.relevant[i]){ rec(i+1,cost); return;} for(int x=0;x<=I.C[i];x++){ a[i]=x; rec(i+1,cost+x);} a[i]=0; }; rec(0,0); }
int solve(int j, const State& st){
  if(j==7) return 0; Key key{j,st}; auto it=memo.find(key); if(it!=memo.end()) return it->second;
  int m=budget[j]*M; Info I=info(j,st);
  if(m==0){ map<int,int> mp; for(size_t i=0;i<I.T.size();i++) addType(mp,I.T[i],I.C[i],j+1); int v=solve(j+1,State(mp.begin(),mp.end())); memo[key]=v; return v; }
  int best=INT_MAX;
  proverMoves(I,[&](const vector<int>&a,int cost){ if(cost>=best) return; int worst=cost; advReplies(I,a,m,[&](const vector<int>&r){ if(worst>=best) return; int v=solve(j+1,nextState(j,I,r,m)); if(v>worst) worst=v; }); if(worst<best) best=worst; });
  memo[key]=best; return best; }
string lname(int l){ string s; for(int t=0;t<7;t++) if((lineMask[l]>>t)&1) s+=char('0'+t); return s; }
string tname(int T){ // print as the pattern-ish: live lines
  string s="{"; bool f=true; for(int l=0;l<NL;l++) if((T>>l)&1){ if(!f) s+=","; s+=lname(l); f=false;} return s+"}"; }
string sname(const State& st){ string s; for(auto&p:st){ s+=tname(p.first)+":"+to_string(p.second)+" "; } return s; }
int main(int argc,char**argv){ string ls=argv[1]; stringstream ss(ls); string w; int li=0; while(ss>>w){ int mk=0; for(char c:w) mk|=1<<(c-'0'); lineMask[li++]=mk; }
  string b=argv[2]; for(int i=0;i<7;i++) budget[i]=b[i]-'0'; M=atoi(argv[3]); int j=atoi(argv[4]);
  // state given as list of "livelines:count" where livelines like 036,345
  State st; map<int,int> mp;
  for(int k=5;k<argc;k++){ string t=argv[k]; size_t c=t.find(':'); string ll=t.substr(0,c); int cnt=atoi(t.substr(c+1).c_str()); int T=0; stringstream s2(ll); string item; while(getline(s2,item,',')){ int mk=0; for(char ch:item) mk|=1<<(ch-'0'); for(int l=0;l<7;l++) if(lineMask[l]==mk) T|=1<<l; } mp[T]+=cnt; }
  st=State(mp.begin(),mp.end());
  int v=solve(j,st); printf("state %s at step %d: value %d\n", sname(st).c_str(), j, v);
  Info I=info(j,st); int m=budget[j]*M;
  proverMoves(I,[&](const vector<int>&a,int cost){ if(cost>v) return; int worst=cost; vector<int> wr; advReplies(I,a,m,[&](const vector<int>&r){ int w2=solve(j+1,nextState(j,I,r,m)); if(w2>worst){worst=w2; wr=r;} });
    if(worst==v){ string as; for(size_t i=0;i<a.size();i++) if(a[i]) as+=tname(I.T[i])+":"+to_string(a[i])+" "; printf("  optimal prover move: avoid [%s] cost %d\n", as.c_str(), cost); } });
}
