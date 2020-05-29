#include<bits/stdc++.h>
using namespace std;
struct bottle{
  int name;
  int litter;
  static bool Litter(bottle a,bottle b){return a.litter <b.litter;}
};
int drink_E(vector<int> &start)
{
    int t = 0;
    while(start[t]==0)
      t++;
    start[t]-=1;
    return t;
}
int drink_W(vector<int> &start)
{
    int max = start.back();
    int t = 0;
    while(start[t]<max)
      t++;
    start[t]-=1;
    return t;
}
int main(){
  int n,m,k,i;
  cin>>n>>m>>k;
  vector<string> guess;
  vector<int> has_drunk;
  cin.ignore();

  vector<int> s;    //start state
  vector<bottle> e; //end state
  string str;
  getline(cin,str);
  stringstream ss(str);
  while(getline(ss,str,' '))
  {
      guess.push_back(str);
      has_drunk.push_back(0);
  }
  for(i = 0;i<m;i++)
  {
    s.push_back(k);
    int t;
    cin>>t;
    bottle x;
    x.name = i;
    x.litter = t;
    e.push_back(x);
  }
  sort(e.begin(),e.end(),bottle::Litter);
  for(i =0;i<guess.size();i++)
  {

    switch (guess[i][0]) {
      case 'E':
        has_drunk[i] = drink_E(s);
        break;
      case 'W':
        has_drunk[i] = drink_W(s);
        break;
    }
  }
  for(i =0;i<guess.size();i++)
  {
      cout<<(e[has_drunk[i]].name+1)<<" ";
  }
  return 0;
}
