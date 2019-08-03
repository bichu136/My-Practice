#include"Jobs-SQLiteManage.h"
using namespace std;
SQLiteManage *SQLraw;
void menu(){
    cout<<"1.Begin a Job\n"
        <<"2.List of Jobs\n"
        <<"3.Read Diary\n"
        <<"4.Today Done\n"
        <<"0.Quit\n";
}
void CVAddingForm(){
    string MaCV;
    string TenVL;
    int Type;
    int atr;
    int status;
    cout<<"MACV: ";
    cout<<"TenVL: ";
    cout<<"Type: ";
    cout<<"Atr: ";
    cout<<"Status: ";
    CV adding(MaCV,TenVL,Type,atr,status,SQLraw->UpdateOnJobs());
}
int main(int argc,char* argv)
{
//------OPEN DATABASE------//
    
    try
    {
        SQLraw=new SQLiteManage("./DIARY");
    }
    catch(string e){
        cout<< e;
        return 0;
    }
    SQLiteManage &SQL = *SQLraw;
    if(SQL.Db()==NULL){
        cout<<"cannot open database";
        return 0;
    }
    SQL.AddRecordToDiary();
    int choose=1;
    /*
    try{
    SQL.AddRecordToDiary();
    }
    catch(string e){
        cout<<e;
        return 0;
    }
    */
    // while(choose){
    //     menu();
    //     cin>>choose;
    //     switch(choose){
    //         case 1:
    //             SQL.AddJobs();
    //             break;
    //         case 2:
    //             SQL.Seekfor(addingCV);
    //             break;
    //         case 3:
    //             SQL.AddRecordToDiary();
    //             break;
    //         case 4:
    //             SQL.Seekfor();
    //             break;
    //         case 5:
    //             //xemNhatKyNgayTrongDb(db);
    //             break;
    //         default:
    //             break;
    //     }
    // }
//------EXECUTE_STATEMENT----//
//rc=sqlitez3_exec(db,sql,callback,NULL,&zErrmess);
//if(rc!=SQLITE_OK){
//    cout<<zErrmess;
//    sqlite3_free(zErrmess);
//}
//else{
//    cout<<"TABLE CREATE SUCCESS!!";
//}
//sqlite3_close(db);
return 0;
}
