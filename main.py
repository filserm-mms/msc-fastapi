from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()

import os
import configparser
from databases.teradata_mms import Teradata
import platform


environment = 'test'

class Article(BaseModel):
    prod_id: int
    country_d: str
    prod_txt: str
    manu_id: int
    sub_category: int
    ean: str

    class Config:
        schema_extra = {
            "example": {
                "prod_id":      2490314,
                "country_d":    "DE",
                "prod_txt":     "9407577 PS4 500GB BLACK",
                "manu_id":      490000157,
                "sub_category": 3204,
                "ean":          "0711719407577",
            }
        }

@app.get("/")
def read_root():
    return {"key": "value"}

@app.get("/prod_id/{prod_id}", response_model=Article, summary="get a single article")
def get_prod_id(prod_id: int):
    result = get_data(prod_id=prod_id, delete_mark=-1)
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/get_all_articles_germany/{delete_mark}", response_model=Article, summary="get a list of articles - input parameter: delete mark")
def get_all_articles_germany(delete_mark: int):
    """
    **0** - returns all articles with delete mark set to 0 

    **1** - returns all articles with delete mark set to 1    

    **-1** - returns all articles with delete mark set either to 0 or to 1

    """
    sql = get_data(prod_id=0, delete_mark=delete_mark)
    json_compatible_item_data = jsonable_encoder(sql)
    return JSONResponse(content=json_compatible_item_data)


def get_data(prod_id=0, delete_mark=-1):
    result = {}
    if prod_id == 0:
        prod_constraint = ''
    else:
        prod_constraint = f'and prod_org_id in ( {prod_id} )'

    if delete_mark != -1:
        del_mark = delete_mark
    else:
        del_mark = '0,1'
        
    sql = f'''
        select 
        top 10
        prod_org_id as prod_id,
        trim(prod_root_id) as country_d,
        prod_txt,
        manu_id,
        prod_grp_id as sub_category,
        trim(upc_code_max) as ean 

        from ep.prod_all 
        where prod_root_id = 'DE'
        {prod_constraint}
        and delete_mark in ( {del_mark} )
    '''
    print (sql)
    resultset = con.query(sql=sql, columndescriptor=1)
    for row in resultset:
        result['prod_id']        = row['prod_id'] 
        result['country_d']      = row['country_d'] 
        result['prod_txt']       = row['prod_txt'] 
        result['manu_id']        = row['manu_id'] 
        result['sub_category']   = row['sub_category'] 
        result['ean']            = row['ean'] 
    
    print (resultset)

    return resultset
    
def init_vars(environment):
    ##############################################
    ### SETTING GLOBAL VARIABLES
    ##############################################
    ### INPUT variables from config.ini - this can be found in the config folder
    configFolder        = 'databases/config/'        #here lie the config file
    curr_directory      = os.path.dirname(os.path.abspath(__file__))

    config              = configparser.ConfigParser()
    config.read(f'{curr_directory}/{configFolder}/config.ini')

    global emailserver, sender, email_to, email_bcc, log_age, path   #these are set only once and should be available in the global scope
    global host, td_user, td_pass

    config_linux = config['LINUX']
    config_general       = config['GENERAL']
    log_age              = int(config_general['log_age'])

    config               = config[environment.upper()]
    path  = config_linux['path_to_tdconnection'] if platform.system() == "Linux" else config['path_to_tdconnection']
    host                 = config['host']
    td_user              = config['td_user']
    td_pass              = config['td_pass']
    td_pass              = td_pass.split(',')   #if 2 password files were given
    td_pass[1]           = td_pass[1].lstrip()  #remove spaces

def connect_to_db():
    global con, teradata_mms
    con = Teradata(host=host, user=td_user, password_path=path, password_files=td_pass, encrypted='y')
     

init_vars(environment)
connect_to_db()