#include"CV.h"
#include<sqlite3.h>
/* 
 * All functions that have //**  throw a string when Err happen
 */
class SQLiteManage
{
    public:
        SQLiteManage();
        SQLiteManage(string filepath);//**
        SQLiteManage(char* filepath);//**
        sqlite3* Db();
        virtual ~SQLiteManage();
        void AddRecordToDiary(); //**
        void AddJobs(CV &AddingCV);
        void Seekfor(CV &a);
        void Seekfor();
        void UpdateOnJobs(string TableName);
    protected:
        sqlite3 * db;
        sqlite3_stmt* stmt;
        char* zErrmess;
        char** data;
        string sql;
        int rc;
        vector<CV> LoadedCV;
    private:

        void showCV();
        typedef string (*TimeState)();
        string getTime(TimeState timestate);
        static string Now();
        static string Today();
        static string Time();
        static int callbackforInsert(void *,int, char**, char**);
        static int callbackforSeek(void *,int, char**, char**);

};



