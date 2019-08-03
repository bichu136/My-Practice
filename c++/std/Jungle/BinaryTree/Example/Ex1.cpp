#include"./BinaryTree/SearchTree.h"
using namespace std;
int main(){
    SearchTree tree;
    int t;
    do{
        cin>>t;
        if(t>0)
            tree.insert(t);
    }while(t>=0);
    //ExpressionTree tree2;
    tree.output(SearchTree::LNR,"LNR");
    tree.output(SearchTree::NLR,"NLR");
    tree.output(SearchTree::Leaf,"Leaf");
    int count;
    count=tree.count(SearchTree::Leafs);
    cout<<"\n"<< count<<"\n";
    count=tree.count(SearchTree::oneBranchNodes);
    cout<<"\n"<< count<<"\n";
    count=tree.count(SearchTree::twoBranchNodes);
    cout<<"\n"<< count<<"\n";
    count=tree.Height();
    cout<<"\n"<< count<<"\n";
    count=tree.Height();
    cout<<"\n"<< count<<"\n";

}
