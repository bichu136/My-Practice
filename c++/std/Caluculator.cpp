#include <iostream>
#include <vector>
#include <string>
#include <iterator>// thư viên gì đó ko cần thiết
#include <sstream>// thư viện stringstream
#include <stack>
using namespace std;
int getResult(vector<string> firstResult){
    stack<int> Stk;
    for(int i=0; i<firstResult.size();i++){
        if((firstResult[i].back()>='0')&&(firstResult[i].back()<='9')){

            Stk.push(stoi(firstResult[i]));
        }
        if(firstResult[i]=="+")
        {
            int t= Stk.top();Stk.pop();
            t+=Stk.top();Stk.pop();
            Stk.push(t);
        }
        if(firstResult[i]=="-")
        {
            int t= Stk.top();Stk.pop();
            t-=Stk.top();Stk.pop();
            Stk.push(t);
        }
        if(firstResult[i]=="*")
        {
            int t= Stk.top();Stk.pop();
            t*=Stk.top();Stk.pop();
            Stk.push(t);
        }
        if(firstResult[i]=="/")
        {
            int t= Stk.top();Stk.pop();
            t/=Stk.top();Stk.pop();
            Stk.push(t);
        }
        if(firstResult[i]=="^"){
            int t=Stk.top()-1;Stk.pop();
            if(t<0){
                Stk.pop();
                Stk.push(1);
                break;
            }
            int a=Stk.top();Stk.pop();
            int b=a;
            while(t>0){
                b*=a;
                t--;
            }
            Stk.push(b);
        }
    }
    return Stk.top();
}
void updatePrio(std::stack<string> Stk,int &prio){
    if(Stk.empty())
    {
        prio=0;
        return;
    }
    if(Stk.top()=="+")
        prio=1;
    if(Stk.top()=="-")
        prio=1;
    if(Stk.top()=="*")
        prio=2;
    if(Stk.top()=="/")
        prio=2;
    if(Stk.top()=="^")
        prio=3;
    if(Stk.top()=="(")
        prio=0;
}
vector<string> RPNConverter(std::vector<string> input){
    vector<string> firstResult;
    stack<string> StkOp;
    int prio=0;
    for (int i = 0; i < input.size(); i++)
    {
        //cout<<"-";
        if((input[i].back()>='0')&&(input[i].back()<='9')){
            firstResult.push_back(input[i]);
        }
        if(input[i]=="+")
        {
            int pri = 1;
            while(pri<=prio){
                string t = StkOp.top();
                firstResult.push_back(t);StkOp.pop();
                updatePrio(StkOp,prio);
            }
            StkOp.push(input[i]);
            prio=pri;
        }
        if(input[i]=="-")
        {
            int pri =1;
            while(pri<=prio){
                string t = StkOp.top();
                firstResult.push_back(t);StkOp.pop();
                updatePrio(StkOp,prio);
            }
            StkOp.push(input[i]);
            prio=pri;
        }
        if(input[i]=="*")
        {
            int pri=2;
            while(pri<=prio){
                string t = StkOp.top();
                firstResult.push_back(t);StkOp.pop();
                updatePrio(StkOp,prio);
            }
            StkOp.push(input[i]);
            prio=pri;
        }
        if(input[i]=="/")
        {
            int pri =2;
            while(pri<=prio){
                string t = StkOp.top();
                firstResult.push_back(t);StkOp.pop();
                updatePrio(StkOp,prio);
            }
            StkOp.push(input[i]);
            prio=pri;
        }
        if(input[i]=="(")
        {
            int pri =0;
            StkOp.push(input[i]);
            prio=pri;
        }
        if(input[i]=="^"){
            int pri= 3;
            while(pri<=prio){
                string t = StkOp.top();
                firstResult.push_back(t);StkOp.pop();
                updatePrio(StkOp,prio);
            }
            StkOp.push(input[i]);
            prio=pri;
        }
        if(input[i]==")")
        {
            while(StkOp.top()!="(")
            {
                firstResult.push_back(StkOp.top());StkOp.pop();
            }
            StkOp.pop();
        }
        updatePrio(StkOp,prio);
    }
    while(!StkOp.empty()){
        firstResult.push_back(StkOp.top());StkOp.pop();
    }
    for (int i = 0; i <firstResult.size(); ++i)
    {
        cout<<firstResult[i]<<" ";
    }
    return firstResult;
}
int main()
{
    string TempInput,t;

    getline(cin,TempInput);
    istringstream StrStrmTemp(TempInput);
    vector<string> input;
    while(getline(StrStrmTemp,t,' '))
        input.push_back(t);
    std::vector<string> RPN;
    RPN = RPNConverter(input);
    cout<<getResult(RPN)<<endl;
    return 0;
}
