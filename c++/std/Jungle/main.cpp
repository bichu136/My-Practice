#include"./BinaryTree/expressionTree.h"
using namespace std;
int main(){
    string expression;
    getline(cin,expression);
    ExpressionTree tree(ExpressionTree::ReversePorlishNotation,expression);
    tree.output(ExpressionTree::LNR,"LNR");
    tree.output(ExpressionTree::NLR,"NLR");
    tree.output(ExpressionTree::Leaf,"Leaf");
    try{
        cout<<tree.Solve()<<"\n";
        cout<<tree.Solve();
    }
    catch(string s){
        cout<<s;
    }
    cout<<"\n";
    return 0;
}
