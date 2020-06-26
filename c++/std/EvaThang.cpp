#include<bits/stdc++.h>
class Card{
public:
  int value;
  int of;
  Card(int value,int of)
  {
      this->value = value;
      this->of = of;
  }
};
bool cardCompare(Card* a,Card* b)
{
  return a->value<b->value;
}
int getIntOfValue(std::string value)
{
  char number = value[0];
  char type = value[1];
  int a = 0;
  int n = 0;
  switch(number)
  {
      case 'A':
        n++;
      case 'K':
        n++;
      case 'Q':
        n++;
      case 'J':
        n++;
      case 'T':
        n++;
      case '9':
        n++;
      case '8':
        n++;
      case '7':
        n++;
      case '6':
        n++;
      case '5':
        n++;
      case '4':
        n++;
      case '3':
        n++;
      case '2':
        break;
  }
  a+= n*4;
  n=0;
  switch(type)
  {
      case 'C':
        n++;
      case 'B':
        n++;
      case 'R':
        n++;
      case 'N':
        break;
  }
  a+=n;
  return a;
}
void release_mem(std::vector<Card*> &cardList)
{
  for (int i=0; i<cardList.size();i++)
  {
      delete cardList[i];
  }
  cardList.clear();
}
int main()
{
    std::fstream file("abc.txt");
    std::vector<Card*> cards;
    std::string s;
    getline(file,s);
    int t = std::stoi(s);
    int number_of_card;
    while (t>0){
      getline(file,s);
      getline(file,s);
      number_of_card = stoi(s);
      //get Adam cards
      for(int i=0; i< number_of_card;i++)
      {
        getline(file,s);
        int v = getIntOfValue(s);
        cards.push_back(new Card(v,0));
      }
      //get Eva cards
      for(int i=0; i< number_of_card;i++)
      {
        getline(file,s);
        int v = getIntOfValue(s);
        cards.push_back(new Card(v,1));
      }
      //sort all cards
      std::sort(cards.begin(),cards.end(),cardCompare);
      std::vector<Card*> temp = cards;
      //counting
      int c=0;
      int old_size;
      do {
        old_size = temp.size();
        int i = 0;
        int k = temp.size()-1;
        while(i<(k)){
          if (temp[i]->of<temp[i+1]->of){
              temp.erase(temp.begin()+i+1);
              temp.erase(temp.begin()+i);
              c++;
              i--;
          }
          k = temp.size()-1;
          i++;
        }
      } while(old_size != temp.size());
      std::cout<<c<<"\n";
      release_mem(cards);
      t--;

    }
    return 0;
}
