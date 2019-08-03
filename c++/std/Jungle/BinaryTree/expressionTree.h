#include"BinaryTree.h"
using namespace std;
class ExpressionTree:public BinaryTree<string>
{
    int pw(int a,int b){
        if (b == 0)
       return 1;
   else if (b % 2 == 0)
       return pw(a, b / 2) * pw(a, b / 2);
   else
       return a * pw(a, b / 2) * pw(a, b / 2);
    }
    static void createSubTree(std::stack<node<string>*> &StkOp,std::stack<node<string>*> &res){
        node<string>* r=res.top();res.pop();
        node<string>* l=res.top();res.pop();
        node<string>* nd=StkOp.top();StkOp.pop();
        nd->l=l;
        nd->r=r;
        res.push(nd);
    }
    static void updatePrio(std::stack<node<string>*> &Stk,int &prio){
        if(Stk.empty())
        {
            prio=0;
            return;
        }
        if(Stk.top()->info=="+")
            prio=1;
        if(Stk.top()->info=="-")
            prio=1;
        if(Stk.top()->info=="*")
            prio=2;
        if(Stk.top()->info=="/")
            prio=2;
        if(Stk.top()->info=="^")
            prio=3;
        if(Stk.top()->info=="(")
            prio=0;
    }
    void getResult(node<string>* c){
        if(c==NULL) return;
        getResult(c->l);
        getResult(c->r);
        if(c->l!=NULL && c->r!=NULL){
            int lt=stoi(c->l->info);
            int rt=stoi(c->r->info);
            int res;
            if(c->info=="+"){
                res=rt+lt;
            }
            if(c->info=="-"){
                res=lt-rt;
            }
            if(c->info=="*"){
                res=lt*rt;
            }
            if(c->info=="/"){
                res=lt/rt;
            }
            if(c->info=="^"){
              res=pw(lt,rt);
            }
            c->info= to_string(res);
            delete c->l;
            delete c->r;
            c->l=NULL;
            c->r= NULL;
        }
    }
public:
    typedef node<string>* (*Input)(vector<string>);
    static node<string>* ReversePorlishNotation(vector<string> ReversePorlishNotation){
        stack<node<string>*> Stk;
        for (size_t i = 0; i < ReversePorlishNotation.size(); i++)
        {
            if((ReversePorlishNotation[i].back()>='0')&&(ReversePorlishNotation[i].back()<='9')){
                Stk.push(new node<string>(ReversePorlishNotation[i]));
            }
            if(ReversePorlishNotation[i]=="+")
            {
                node<string> * t=new node<string>(ReversePorlishNotation[i]);
                t->l=Stk.top();Stk.pop();
                t->r=Stk.top();Stk.pop();
                Stk.push(t);
            }
            if(ReversePorlishNotation[i]=="-")
            {
                node<string> * t=new node<string>(ReversePorlishNotation[i]);
                t->l=Stk.top();Stk.pop();
                t->r=Stk.top();Stk.pop();
                Stk.push(t);
            }
            if(ReversePorlishNotation[i]=="*")
            {
                node<string> * t=new node<string>(ReversePorlishNotation[i]);
                t->l=Stk.top();Stk.pop();
                t->r=Stk.top();Stk.pop();
                Stk.push(t);
            }
            if(ReversePorlishNotation[i]=="/")
            {
                node<string> * t=new node<string>(ReversePorlishNotation[i]);
                t->l=Stk.top();Stk.pop();
                t->r=Stk.top();Stk.pop();
                Stk.push(t);
            }
            if(ReversePorlishNotation[i]=="^")
            {
                node<string> * t=new node<string>(ReversePorlishNotation[i]);
                t->l=Stk.top();Stk.pop();
                t->r=Stk.top();Stk.pop();
                Stk.push(t);
            }
        }
        node<string>* res=Stk.top();Stk.pop();
        return res;
    }
    static node<string>* RegularExpression(vector<string> expression){
        stack<node<string>*> res;
        stack<node<string>*> StkOp;
        int prio=0;
        for (int i = 0; i < expression.size(); i++)
        {
            if((expression[i].back()>='0')&&(expression[i].back()<='9')){
                res.push(new node<string>(expression[i]));
            }
            if(expression[i]=="+")
            {
                int pri = 1;
                while(pri<=prio){
                    createSubTree(StkOp,res);
                    updatePrio(StkOp,prio);
                }
                StkOp.push(new node<string>(expression[i]));
                prio=pri;
            }
            if(expression[i]=="-")
            {
                int pri = 1;
                while(pri<=prio){
                    createSubTree(StkOp,res);
                    updatePrio(StkOp,prio);
                }
                StkOp.push(new node<string>(expression[i]));
                prio=pri;
            }
            if(expression[i]=="*")
            {
                int pri=2;
                while(pri<=prio){
                    createSubTree(StkOp,res);
                    updatePrio(StkOp,prio);
                }
                StkOp.push(new node<string>(expression[i]));
                prio=pri;
            }
            if(expression[i]=="/")
            {
                int pri = 2;
                while(pri<=prio){
                    createSubTree(StkOp,res);
                    updatePrio(StkOp,prio);
                }
                StkOp.push(new node<string>(expression[i]));
                prio=pri;
            }
            if(expression[i]=="(")
            {
                int pri =0;
                StkOp.push(new node<string>(expression[i]));
                prio=pri;
            }
            if(expression[i]=="^"){
                int pri = 3;
                while(pri<=prio){
                    createSubTree(StkOp,res);
                    updatePrio(StkOp,prio);
                }
                StkOp.push(new node<string>(expression[i]));
                prio=pri;
            }
            if(expression[i]==")")
            {
                while(StkOp.top()->info!="(")
                {
                    createSubTree(StkOp,res);
                }
                delete StkOp.top();
                StkOp.pop();
            }
            updatePrio(StkOp,prio);
        }
        while(!StkOp.empty()){
            createSubTree(StkOp,res);
        }
        node<string>* Res=res.top();res.pop();
        return Res;
    }
    ExpressionTree():BinaryTree(){}
    ExpressionTree(Input type,string expression){
        istringstream StrStrmTemp(expression);
        vector<string> input;
        string t;
        while(getline(StrStrmTemp,t,' '))
            input.push_back(t);
        root = type(input);
    }
    ExpressionTree(string expression){
        istringstream StrStrmTemp(expression);
        vector<string> input;
        string t;
        while(getline(StrStrmTemp,t,' '))
            input.push_back(t);
        //buildTree(input);
    }
    int Solve(){
        if(root){
        node<string>* c=root;
        getResult(c);
        int res=stoi(c->info);
        delete c;
        root=NULL;
        return res;
        }
        string s="nothing in this tree to calculate";
        throw s;
    }
};
