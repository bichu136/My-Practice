#include<iostream>
#include<cstring>
#include<stack>
using namespace std;
class node{
public:
    int info;
    node* l;
    node* r;
    node(){
        l=NULL;
        r=NULL;
    }
    node(int x){
        info=x;
        l=NULL;
        r=NULL;
    }

};
class Tree{
    node* root;
public:
    Tree(){
        root=NULL;
    }
    void insert(int x){
        node* c=root;
        node* p=NULL;
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
            if(p->l==c)
                p->l=new node(x);
            else
                p->r=new node(x);
        }
        else{
            root=new node(x);
        }
    }
    typedef void (*TreeOut)(node*);
    typedef int (*Counter)(node*);

    int count(Counter function){
        stack<node*> Stknode;
        Stknode.push(root);
        node* c=NULL;
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
    static int Node(node* c){
        return 1;
    }
    static int Leaf(node* c){
            if(c->l==NULL && c->r==NULL){
                return 1;
            }
            return 0;
    }
    static int oneBranchNode(node* c){
            if(c->l==NULL ^ c->r==NULL){
                return 1;
            }
            return 0;
    }
    static int twoBranchNode(node* c){
            if(c->l!=NULL & c->r!=NULL){
                return 1;
            }
            return 0;
    }
    ///--------OUTPUT-------------//
    static void LNR(node* Tree){
        if(Tree!=NULL)
        {
            LNR(Tree->l);
            cout<<Tree->info<<" ";
            LNR(Tree->r);
        }
        }
    static void NLR(node* Tree){
        if(Tree!=NULL)
        {
            cout<<Tree->info<<" ";
            NLR(Tree->l);
            NLR(Tree->r);
        }
    }
    static void LRN(node* Tree){
        if(Tree!=NULL)
        {
            LRN(Tree->l);
            LRN(Tree->r);
            cout<<Tree->info<<" ";
        }
    }
    void output(TreeOut function,string name){
        node* c = root;
        cout<<"Ouput type:"<<name<<"\n";
        function(c);
        cout<<"\n---------------\n";
    }
    int countLeaf(node* Tree){
        if(Tree==NULL) return 0;
        if(Tree->l==NULL && Tree->r==NULL) return 1;
        return countLeaf(Tree->l)+countLeaf(Tree->r);
    }

    int count_1BranchNode(node* Tree){
        if(Tree==NULL) return 0;
        if(Tree->l==NULL ^ Tree->r==NULL){
            return count_1BranchNode(Tree->l)+count_1BranchNode(Tree->r)+1;
        }
        return count_1BranchNode(Tree->l)+count_1BranchNode(Tree->r);
    }
    int count_2BranchNode(node* Tree){
        if(Tree==NULL) return 0;
        if(Tree->l!=NULL && Tree->r!=NULL){
            return count_2BranchNode(Tree->l)+count_2BranchNode(Tree->r)+1;
        }
        return count_2BranchNode(Tree->l)+count_2BranchNode(Tree->r);
    }

    int countEven(node* Tree){
        if(Tree==NULL) return 0;
        if(Tree->info%2==0) return countEven(Tree->l)+countEven(Tree->r)+1;
        return countEven(Tree->l)+countEven(Tree->r);
    }

    int countOdd(node* Tree){
        if(Tree==NULL) return 0;
        if(Tree->info%2) return countOdd(Tree->l)+countOdd(Tree->r)+1;
        return countOdd(Tree->l)+countOdd(Tree->r);
    }

    void rotateRight(node* Tree){
        node* p=Tree->l;
        if(p!=NULL){
            Tree->l=p->r;
            p->r=Tree;
            Tree=p;
        }
    }

    void rotateLeft(node* Tree){
        node* p=Tree->r;
        if(p!=NULL){
            Tree->r=p->l;
            p->l=Tree;
            Tree=p;
        }
    }

    int Height(node* Tree,int h=-1){
        if(Tree==NULL) return h;
        int hl=Height(Tree->l,h+1),hr=Height(Tree->r,h+1);
        return (hl>hr)? hl :hr;
    }
};
