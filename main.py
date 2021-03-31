from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

import os
import configparser
from teradata.teradata_mms import Teradata
import platform
environment = 'test'

class Prod(BaseModel):
    prod_txt: str
    prod_manu_txt: str

@app.get("/")
def read_root():
    return {"key": "value"}


@app.get("/prod_id/{prod_id}")
def get_prod_id(prod_id: int):
    results = []
    sql = f"select prod_txt, prod_manu_txt from ep.prod_all where prod_id = {prod_id}"
    resultset = con.query(sql=sql)
    for row in resultset:
        prod_txt      = row[0]
        prod_manu_txt = row[1]
    return {"prod_txt": prod_txt, "prod_manu_txt": prod_manu_txt}





def init_vars(environment):
    ##############################################
    ### SETTING GLOBAL VARIABLES
    ##############################################
    ### INPUT variables from config.ini - this can be found in the config folder
    configFolder        = 'teradata/config/'        #here lie the config file
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