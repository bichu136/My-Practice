#include "Jobs-SQLiteManage.h"
/*      sqlite3 * db;     // pointer sqlite3 to access and use sqlite
 *      char* zErrmess;  // a string for error message from sqlite
 *      char* sql;      // a string to create sql statement;
 *      char* data;    // something use in callback function
 *      int rc;       // a interger for index of error when do something with sqlite,
 */
using namespace std;
SQLiteManage::SQLiteManage(){
    db=NULL;
    zErrmess=NULL;
}
SQLiteManage::SQLiteManage(string filepath)
{
    zErrmess==NULL;
    rc=sqlite3_open(filepath.c_str(),&db);
    if(rc){
        db=NULL;
        return;
    }

    sql="SELECT * FROM JOBS;";
    rc=sqlite3_prepare_v2(db,sql.c_str(),-1,&stmt,NULL);
    if(rc!=SQLITE_OK){
        cout<< sqlite3_errmsg(db);
    }
    cout<<"\n-----\n";
    while((rc=sqlite3_step(stmt))==SQLITE_ROW){	
    string MaCV(reinterpret_cast<const char*>(sqlite3_column_text(stmt,0)));
    string Name(reinterpret_cast<const char*>(sqlite3_column_text(stmt,1)));
    string Atribute(reinterpret_cast<const char*>(sqlite3_column_text(stmt,2)));
    string Type(reinterpret_cast<const char*>(sqlite3_column_text(stmt,3)));
    string Status(reinterpret_cast<const char*>(sqlite3_column_text(stmt,4)));
    string LastUpDate(reinterpret_cast<const char*>(sqlite3_column_text(stmt,5)));
    int atr=(Atribute!="")? stoi(Atribute):-1 ;
    int type=(Type!="")? stoi(Type):-1;
    int status=(Status!="")? stoi(Status):-1;
    LoadedCV.push_back(CV(MaCV,Name,atr,type,status,LastUpDate));
//	sqlite3_clear_bindings(stmt);
    }
    if(rc!=SQLITE_DONE){
    cout<<"Fail";
    }
    sqlite3_finalize(stmt);
}
SQLiteManage::SQLiteManage(char* filepath)
{
    rc=sqlite3_open(filepath,&db);
    if(rc){
        db=NULL;
    }
    sql="SELECT * FROM JOBS;";
    rc=sqlite3_prepare_v2(db,sql.c_str(),-1,&stmt,NULL);
    if(rc!=SQLITE_OK){
       
        cout<< sqlite3_errmsg(db);
    }
     cout<<"\n-----\n";
     while((rc=sqlite3_step(stmt))==SQLITE_ROW){	
        string MaCV(reinterpret_cast<const char*>(sqlite3_column_text(stmt,0)));
        //string Name(reinterpret_cast<const char*>(sqlite3_column_text(stmt,1)));
        string Name="ten";
        string Atribute(reinterpret_cast<const char*>(sqlite3_column_text(stmt,2)));
        string Type(reinterpret_cast<const char*>(sqlite3_column_text(stmt,3)));
        string Status(reinterpret_cast<const char*>(sqlite3_column_text(stmt,4)));
        string LastUpDate(reinterpret_cast<const char*>(sqlite3_column_text(stmt,5)));
        int atr=(Atribute!="")? stoi(Atribute):-1 ;
        int type=(Type!="")? stoi(Type):-1;
        int status=(Status!="")? stoi(Status):-1;
        LoadedCV.push_back(CV(MaCV,Name,atr,type,status,LastUpDate));
        }
     if(rc!=SQLITE_DONE){
     cout<<"Fail";
     }
     sqlite3_finalize(stmt);
}


void SQLiteManage::AddJobs(CV &AddingCV){
    
    sql="INSERT INTO JOBS (MACV,TENVL,ATRIBUTE,STATUS,TYPE,LASTUPDATE) VALUES('"
    + AddingCV.ma() + "','"+  AddingCV.name() + "',"+to_string(AddingCV.atr()) + ","+ to_string(AddingCV.type()) + ","+ to_string(AddingCV.status()) + ",'"+ AddingCV.lastupdate() +"');";
    LoadedCV.push_back(AddingCV);
    if(rc!=SQLITE_OK){
        sqlite3_free(zErrmess);

    }
}


sqlite3* SQLiteManage::Db(){
    return db;
}


string SQLiteManage::getTime(TimeState timestate){
    string result;
    char lastupdate[15];
    time_t Time;
    time(&Time);
    struct tm *timeReader;
    timeReader=localtime(&Time);
    strftime(lastupdate,30,timestate().c_str(),timeReader);
    result=lastupdate;
    return result;
}


string SQLiteManage::Now(){

    return "%d/%m/%y %H:%M";
}


string SQLiteManage::Today(){
    return "%d/%m/%y";
}


string SQLiteManage::Time(){
    return "%H:%M";
}


void SQLiteManage::AddRecordToDiary(){
    if(db==NULL){
        throw "cannot add record due to that database haven't open yet!!";
    }
    cout<<"--\n";
    showCV();
    unsigned int x;
    do{
        cout<<"--";
        cin>>x;
        if(x>=LoadedCV.size()) {cout<<"unexpected job.";}
    }while(x>=LoadedCV.size());
    string now=Now();
    sql="INSERT INTO DIARY VALUES('"+LoadedCV[x].ma()+"','"+getTime(Today)+"','"+getTime(Time)+"','"+getTime(Time)+"','');";
    rc=sqlite3_exec(db,sql.c_str(),callbackforInsert,NULL,&zErrmess);
    if(rc!=SQLITE_OK){
        string Err=zErrmess;
        sqlite3_free(zErrmess);
        throw Err;
    }

}


void SQLiteManage::showCV(){
    for(int i=0;i<LoadedCV.size();i++){
    cout<<i<<"."<<LoadedCV[i].ma()<<"|"<<LoadedCV[i].name()<<"\n";
    }
}


SQLiteManage::~SQLiteManage()
{
    sqlite3_close(db);
}


int SQLiteManage::callbackforInsert(void *NotUsed, int argc, char **argv, char **azColName){
    return 0;
}
