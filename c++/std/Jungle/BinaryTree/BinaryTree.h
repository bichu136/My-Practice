#include<iostream>
#include<cstring>
#include<stack>
#include<vector>
#include<istream>
#include <sstream>
#include"nodeBinaryTree.h"

using namespace std;
template<class T>
class BinaryTree{

protected:
  node<T>* root;
  int countHeight(node<T>* Tree,int h=-1){
        if(Tree==NULL) return h;
        int hl=countHeight(Tree->l,h+1),hr=countHeight(Tree->r,h+1);
        return (hl>hr)? hl :hr;
    }
public:
  BinaryTree(){
        root=NULL;
  }

  typedef void (*TreeOut)(node<T>*);
  typedef void (*TreeOutInt)(node<T>*,int);
  typedef int (*Counter)(node<T>*);

  int count(Counter function){
        stack<node<T>*> Stknode;
        Stknode.push(root);
        node<T>* c=NULL;
        int counter=0;
        while(!Stknode.empty())
        {
            c=Stknode.top();Stknode.pop();
            counter+=function(c);
            if(c->r!=NULL) Stknode.push(c->r);
            if(c->l!=NULL) Stknode.push(c->l);
        }
        return counter;
    }
    static int Nodes(node<T>* c){
        return 1;
    }
    static int Leafs(node<T>* c){
            if(c->l==NULL && c->r==NULL){
                return 1;
            }
            return 0;
    }
    static int oneBranchNodes(node<T>* c){
            if(c->l==NULL ^ c->r==NULL){
                return 1;
            }
            return 0;
    }
    static int twoBranchNodes(node<T>* c){
            if(c->l!=NULL & c->r!=NULL){
                return 1;
            }
            return 0;
    }
    ///--------OUTPUT-------------//
    static void LNR(node<T>* Tree){
        if(Tree!=NULL)
        {
            LNR(Tree->l);
            cout<<Tree->info<<" ";
            LNR(Tree->r);
        }
    }
    static void NLR(node<T>* Tree){
        if(Tree!=NULL)
        {
            cout<<Tree->info<<" ";
            NLR(Tree->l);
            NLR(Tree->r);
        }
    }
    static void LRN(node<T>* Tree){
        if(Tree!=NULL)
        {
            LRN(Tree->l);
            LRN(Tree->r);
            cout<<Tree->info<<" ";
        }
    }
    static void Leaf(node<T>*c){
        if(c!=NULL)
        {
            Leaf(c->l);
            if(c->l==NULL && c->r==NULL)
                cout<<c->info<<" ";
            Leaf(c->r);
        }
    }
    static void NodeAtLevel(node<T>* c,int x){
        if(c!=NULL)
        {
            NodeAtLevel(c->r,x-1);
            if(x==0)
                cout<<c->info<<" ";
            NodeAtLevel(c->l,x-1);
        }
    }
    void output(TreeOut function,string name){
        node<T>* c = root;
        cout<<"Ouput type:"<<name<<"\n";
        function(c);
        cout<<"\n---------------\n";
    }
    void output(TreeOutInt function,int x,string name){
        node<T>* c = root;
        cout<<"Ouput type:"<<name<<"\n";
        function(c,x);
        cout<<"\n---------------\n";
    }
    //----------------------------------------//
    int Height(){
          node<T>* c = root;
          return countHeight(c);
    }

};
