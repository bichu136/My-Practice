#include"BinaryTree.h"
using namespace std;
class ExpressionTree:public BinaryTree<string>
{
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
            c->info= to_string(res);
            delete c->l;
            delete c->r;
            c->l=NULL;
            c->r= NULL;
        }
    }
public:
    ExpressionTree():BinaryTree(){
    }
    ExpressionTree(vector<string> ReversePorlishNotation){
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
        root=Stk.top();Stk.pop();
    }
    int Solve(){
        node<string>* c=root;
        getResult(c);
        int res=stoi(c->info);
        delete c;
        root=NULL;
        return res;
    }
};
