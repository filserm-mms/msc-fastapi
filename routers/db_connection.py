import os, platform
import configparser
from databases.teradata_mms import Teradata

def init_vars(environment):
    ##############################################
    ### SETTING GLOBAL VARIABLES
    ##############################################
    ### INPUT variables from config.ini - this can be found in the config folder
    configFolder        = '../databases/config/'        #here lie the config file
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
    if platform.system() == "Linux":
        con = Teradata(host=host, user=td_user, gcp_project_id = 'mms-msc-msc-d-fx5e', gcp_secret_password='td_dwh4test_pp_user_pwd')
    else:
        con = Teradata(host=host, user=td_user, password_path=path, password_files=td_pass, encrypted='y')

    return con

environment = "test"
init_vars(environment)
con = connect_to_db()
