#include"BinaryTree.h"
using namespace std;
class SearchTree:public BinaryTree<int>{
    void rotateRight(){
        node<int>* p=root->l;
        if(p!=NULL){
            root->l=p->r;
            p->r=root;
            root=p;
        }
    }
    void rotateLeft(){
        node<int>* p=root->r;
        if(p!=NULL){
            root->r=p->l;
            p->l=root;
            root=p;
        }
    }
public:
    SearchTree(){
        root=NULL;
    }
    void insert(int x){
        node<int>* c=root;
        node<int>* p=NULL;
        while(c!=NULL){
            if(c->info==x)
                return;
            p=c;
                if(c->info>x)
                    c=c->l;
               else
                    c=c->r;
        }
        if(p!=NULL){
            if(p->info>x)
                p->l=new node<int>(x);
            else
                p->r=new node<int>(x);
        }
        else{
            root=new node<int>(x);
        }
    }
    //---------UNDONE----------//
    void balance(node<int>* Tree){
        int hl=countHeight(Tree->l)+1,hr=countHeight(Tree->r)+1;
        int t=(hl-hr);
        if(t>0)
            while(t>1){
                rotateRight();
                t--;t--;
            }
        else
            while(t<-1){
                rotateLeft();
                t++;t++;
            }
    }
    void balanceTree(){
        node<int>*c=root;
        balance(c);
    }
};
