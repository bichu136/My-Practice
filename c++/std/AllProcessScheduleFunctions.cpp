#include<bits/stdc++.h>
using namespace std;


//----------------TYPEDEF--------------------///
typedef void (*func)();
//------------------------CLASSES-----------//
class process
{
public:
  string name;
  int at;
  int bt;
  int priority;
  int start_time;
  int end_time;
  int rt;
  int wt;
  int tt;
  process();
  process(string Name,int bt,int at=0, int priority = 0)
  {
    name = Name;this->at=at;this->bt=bt;this->priority=priority;start_time = -1;;wt=0;
  }
  static bool Priority(process* p1,process* p2){ return (p1->priority<p2->priority);}
  static bool ArrivalTime(process* p1,process* p2){ return (p1->at<p2->at);}
  static bool Burstime(process* p1,process* p2){ return (p1->bt<p2->bt);}
  string ToString(){return this->name +"\t" + to_string(this->at)+"\t" +to_string(this->bt)+"\t" +to_string(this->priority)+"\t"+to_string(this->tt)+"\t"+to_string(this->rt)+"\t"+to_string(this->wt);}
};
//----------GLOBAL VARIABLE-----------------//
std::vector<process*> processes;
int n,b1,b2,c;
vector<process*> r;
vector<process*> q;
bool has_new_process;
int qt = 4;
int t;
// int ProcessScheduleFunctions::qt = 0;
// int ProcessScheduleFunctions::t = 0;
// bool ProcessScheduleFunctions::has_new_process=false;

//-------------FUNCTIONS---------------------//

void Gant(vector<process*> processes,func x)
{
  sort(processes.begin(),processes.end(),process::ArrivalTime);
  int i;
  vector<process*> temp=processes;
  q.push_back(processes[0]);
  r.push_back(processes[0]);
  t = processes[0]->at;
  processes[0]->start_time = processes[0]->at;
  temp.erase(temp.begin());
  cout<<t<<"\t"<<q[0]->name<<"\n";
  t++;
  do
  {
    has_new_process = false;
    //so what to do during time
    q[0]->bt-=1;
    if (q[0]->bt==0){
      q[0]->rt = q[0]->start_time-q[0]->at;
      q[0]->end_time = t;
      q[0]->tt = t - q[0]->at;
      q.erase(q.begin());
    }
    //check ArrivalTime
    while(temp.empty()==false&&t==temp[0]->at){
      q.push_back(temp[0]);
      temp.erase(temp.begin());
      has_new_process=true;
    }
    //sort with all new component
    x();
    //
    bool is_change_process_active=false;
    if (r[r.size()-1] != q[0]){
        if (q[0]->start_time < 0)
          q[0]->start_time = t;
        r.push_back(q[0]);
        is_change_process_active = true;
    }
    for (i=1;i<q.size();i++){
      q[i]->wt+=1;
    }
    string b="";
    if (is_change_process_active)
      for (i=0;i<q.size();i++){
        b= b+q[i]->name+" ";
      }
    cout<<t<<" "<<b<<"\n";
    t++;
  }while(q.empty()==false);
}
void srt(){
    if (has_new_process){
    sort(q.begin(),q.end(),process::Burstime);
    }
}
void rr(){
    if (q.empty()==false)
      if (t%qt==0)
      {
          //round robin
          process* z = q[0];
          q.erase(q.begin());
          q.push_back(z);
        }
}
void sjf(){
  if (has_new_process){
  sort(q.begin()+1,q.end(),process::Burstime);
  }
}


void process_input()
{
  string name;
  int at,bt,prio;
  while (n>0)
  {
    cin.ignore();
    getline(cin,name);
    cin>>at;
    cin>>bt;
    cin>>prio;
    processes.push_back(new process(name,bt,at,prio));

    n--;
  }
}
void print()
{
    cout<< "name\tat\tbt\tpri\ttt\trt\twt\n";
    sort(processes.begin(),processes.end(),process::ArrivalTime);
    for(int i=0;i<processes.size();i++)
    {
      string t =processes[i]->ToString();
      cout<<t<<"\n";
    }

}
int main()
{
  cout<< "how many processes do we need to schedule?(number)";
  cin >> n;
  process_input();
  func x;
  cout<< "choose Functions:\n1. srt\n2. sjf \n3. rr ";
  cin>>c;
  switch(c)
  {
    case 1:
      x = srt;
      break;
    case 2:
      x = sjf;
      break;
    case 3:
      x = rr;
      break;
  }


  Gant(processes,x);
  cout<<"\n--------------------------------\n";
  print();
  return 0;
}
