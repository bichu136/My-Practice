#include "CV.h"

CV::CV()
{
    //ctor
}
CV::CV(string&ma,string&name,int&atr,int&type,int&status,string &lastupdate)
{
    MaCV = ma;
    Atribute = atr;
    Type = type;
    Name = name;
    Status = status;  
    LastUpDate=lastupdate;
}
string CV::ma(){return MaCV;}

string CV::name(){return Name;}

int CV::atr(){return Atribute;}

int CV::type(){return Type;}

int CV::status(){return Status;}

string CV::lastupdate(){return LastUpDate;}
void CV::update(string lastupdate){
    LastUpDate=lastupdate;
}
CV::~CV()
{
    //dtor
}
