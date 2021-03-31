# @Author: Michael Filser, Lukas Gruber
# @Date:   25-09-2020
# @Last modified time: 2021-03-01 15:14:30

from google.cloud.bigquery.job import query
from teradatasql import *

class Teradata():

    def __init__(self, host, user, password=None, password_path=None, password_files=None, encrypted='n'):
        self.host     = host
        self.user     = user
        self.password = f'ENCRYPTED_PASSWORD(file:{password_path}{password_files[0]},file:{password_path}{password_files[1]})' if encrypted == 'y' else password
        self.con = self.get_connection()

    def get_connection(self):
        try:
            print(f'connecting to database {self.host}...')
            con = connect(host=self.host, user=self.user, password=self.password, logmech="TD2")
        except Exception as error:
            print(f'Error: connection not established {error}')
            Teradata._instance = None
        else:
            print(f'connection established to {self.host}')
            return con

    def __repr__(self):
        return f'Teradata class for establishing a connection to {self.host} with user {self.user}'


    def query(self, sql, params=[], sql_name='', querytype='select', errorcodes_to_ignore=None, columndescriptor=0, explainonly=0):

        if explainonly == 1: sql = 'EXPLAIN '+ sql

        try:
            self.con.cursor().execute('select date;')
        except Exception as error:
            print(f'Error: lost connection.. {error}')
            self.con = self.get_connection()


        if querytype == 'select':
            with self.con.cursor() as cur:
                try:
                    cur.execute(sql, params, ignoreErrors=errorcodes_to_ignore)

                    if columndescriptor == 0:
                        resultset = cur.fetchall()
                    else:
                        column_names = [col_desc[0].lower() for col_desc in cur.description]
                        rows         = list(cur.fetchall())
                        resultset    = [dict(zip(column_names, row)) for row in rows]

                except Exception as error:
                    raise Exception({error})
                else:
                    return resultset
        else:
            with self.con.cursor() as cur:
                try:
                    cur.execute(sql, params)
                    numrows = int(cur.rowcount)
                except Exception as error:
                    raise Exception({error})
                else:
                    return 0 if numrows is None else numrows

    def load_csv(self, filename, delimiter, column_cnt, tablename=''):
        import csv
        columns = column_cnt * '?,'
        columns = columns[:-1] #remove last comma

        try:
            with open (filename, encoding='utf-16', newline='') as f:
                with self.con.cursor () as cur:
                    # 
                    #   load into a volatile table if no tablename was given
                    #
                    if tablename == '':                                           
                        columns_vt = []
                        import uuid
                        tablename_uuid = 'vt_'+str(uuid.uuid4()).replace('-','')  #make a unique tablename
                        for i in range(column_cnt):
                            columns_vt.append('field'+ str(i) + ' varchar(300),')
                        columns_vt = ''.join(columns_vt)                   
                        columns_vt = columns_vt[:-1] #remove last comma
                        cur.execute (f'create volatile table {tablename_uuid} ({columns_vt}) on commit preserve rows')
                        cur.execute (f'insert into {tablename_uuid} ({columns})', [ row for row in csv.reader (f, delimiter=delimiter) ])
                        return (tablename_uuid)

                    #
                    #  if a tablename was given, this has to be available on teradata
                    #
                    else:
                        cur.execute (f'insert into {tablename} ({columns})', [ row for row in csv.reader (f, delimiter=delimiter) ])
                    
        except Exception as error:
            raise Exception({error})

    def __del__(self):
        self.con.close()

if __name__ == '__main__':
    #connecting with encrypted password by providing encrypted password files
    #providing first the password key file, then the encrypted password file
    con = Teradata(host='dwh4test', user='filser', password_path='E:/warp/dwh2db/python/', password_files=['Filser_DWHFLASH_PassKey.properties', 'Filser_DWHFLASH_EncPass.properties'], encrypted='y')
    print (con)

    #read from bigquery and load via csv
    from bigquery_mms import BigQuery
    bq_con = BigQuery()
    stmt = "SELECT * FROM `mms-msc-msc-d-fx5e.msc_test.outlet`"
    df = bq_con.query(stmt, fmt='pd')
    #print (df.head(2))

    # export to csv
    filename = 'd:/temp/demo1.csv'
    #tablename = 'test.outlet_full_mf'
    delimiter = '|'
    df.to_csv(filename, index=False, encoding='utf-16', sep = delimiter, header=False)  
    column_cnt=len(df.axes[1])
    
    vt_table = con.load_csv(filename, delimiter, column_cnt)
    queryresult = con.query(sql=f'select * from {vt_table}')
    print (queryresult)

    #connecting with plaintext password - not recommended
    #con = Teradata(host='dwh4test', user='gruberlu', password='********')

    con.__del__()
    #querying an instance
    #queryresult = con.query(sql='select outlet_txt from ep.v_outlet where outlet_id = 466')
    #queryresult = con.query(sql='select 1/0', errorcodes_to_ignore=2618) #<- this ignores the divisionbyzero error_code
    queryresult = con.query(sql='select top 1 create_date from acclog.progadmin_sqls where program_id = 1')
    print (queryresult)

    #insert, delete, update, collect stats, create table/view, stored procedures etc ...
    #from random import *
    #numrows = con.query(querytype='insert', sql=f"inser into test.testtable ({randint(1,9999999)}, 'this is a python generated insert')")
    #numrows = con.query(querytype='stored procedure', sql=r"CALL PP.drop_table_if_exists('test', 'testtable2', outmsg);")
    #print (numrows)

    #sql with user data -> sql with placeholder (?) and values in params
    #queryresult = con.query(sql="select * from test.djangoTest where txt_value = ?;", params=['text'])