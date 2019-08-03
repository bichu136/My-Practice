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
    node<int>*& find(int x){
        node<int> *c=root;
        node<int> *p=NULL;
        while(c!=NULL){
            if(c->info==x){
                if(p==NULL)
                    return root;
                if(c==p->r)
                    return p->r;
                if(c==p->l)
                    return p->l;
            }
            if(x>c->info){
                p=c;
                c=c->r;
            }
            if(x<c->info){
                p=c;
                c=c->l;
            }
        }
        return p->l;
    }
    int MAX(){
        node<int>* c=root;
        node<int>* p=NULL;
        while(c!=NULL){
            p=c;
            c=c->r;
        }
        if(p==NULL)
            return 0;
        else return p->info;
    }
    void remove(int x){
        node<int>* &c=find(x);
        remove(c);
    }
    void remove(node<int>* &c){
        if(c!=NULL){
            if(c->r==NULL && c->l==NULL){
                delete c;
                c=NULL;
                return;
            }
            if(c->r==NULL ^ c->l==NULL){
                if(c->r==NULL){
                    node<int>* t=c;
                    c=c->l;
                    delete t;
                }
                else c=c->r;
            }
            if(c->r!=NULL && c->l!=NULL){
                node<int> *t=c->l;
                node<int> *p=c;
                while(t->r!=NULL){
                    p=t;
                    t=t->r;
                }
                c->info=t->info;
                if(p!=c)
                    remove(p->r);
                else remove(p->l);
            }
        }
    }
    //---------UNDONE----------//
};
