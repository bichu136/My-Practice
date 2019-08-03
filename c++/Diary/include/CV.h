#ifndef CV_H
#define CV_H
#include<bits/stdc++.h>
using namespace std;

class CV
{
    public:
        CV();
        CV(string&ma,string&name,int&atr,int&type,int&status,string &lastupdate);
        string tostring();
        string ma();
        string name();
        int atr();
        int type();
        int status();
        string lastupdate();
        void update(string lastupdate);
        void setCV();
        virtual ~CV();

    protected:

    private:
    string MaCV;
    string Name;
    int Atribute;
    int Type;
    int Status;
    string LastUpDate;
};

#endif // CV_H
