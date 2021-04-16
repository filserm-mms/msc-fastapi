from fastapi import APIRouter, Depends
from fastapi.param_functions import Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import List
from datetime import date, datetime

from dependencies import verify_token
from .db_connection import con

router = APIRouter(
    prefix="/contractMaster",
    tags=["contractMaster"],
    dependencies=[Depends(verify_token)]
)

class Manufacturer(BaseModel):
    manu_id:        int
    manu_txt:       str
    prod_root_id:   str
    update_time:    datetime

    class Config:
        schema_extra = {
            "example": {
                "manu_id":      490006149,
                "manu_txt":     "CARSON",
                "prod_root_id": "DE  ",
                "update_time":  "2021-03-09T09:47:28.301000"
            }
        }

class ManufacturerList(BaseModel):
    date: List[Manufacturer]

    class Config:
        schema_extra = {
            "example": {
                "2021-03-09": [
                        Manufacturer.Config.schema_extra["example"]
                ]
            }
        }


class Supplier(BaseModel):
    sap_kreditor_no:    int
    supp_txt:           str
    prod_root_id:       str
    update_time:        datetime

    class Config:
        schema_extra = {
            "example": {
                "sap_kreditor_no":  823637,
                "supp_txt":         "MICHAEL HUBER/FABIAN FRISCHMANN - GBR DICHT & ERGREIFEND",
                "prod_root_id":     "DE  ",
                "update_time":      "2021-04-15T09:14:45.454000"
            }
        }


class SupplierList(BaseModel):
    date: List[Supplier]

    class Config:
        schema_extra = {
            "example": {
                "2021-04-15": [
                    Supplier.Config.schema_extra["example"]
                ]
            }
        }


@router.get("/manu/{date}", response_model=ManufacturerList, summary="get manufacturers by date")
def get_manufacturers(date: date = Path(None)):
    '''
    **{date}** has to be in the format of **"YYYY-MM-DD"**

    Returns all manufacturers which have been updated since {date}.
    '''
    result = get_manu_data(date)
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)

@router.get("/supplier/{date}", response_model=SupplierList, summary="get suppliers by date")
def get_suppliers(date: date = Path(None)):
    '''
    **{date}** has to be in the format of **"YYYY-MM-DD"**

    Returns all manufacturers which have been updated since {date}.
    '''
    result = get_sup_data(date)
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)

def get_manu_data(date):
    result = {}

    sql = '''
    select
        m.manu_id,
        m.manu_txt,
        m.prod_root_id,
        mm.update_time
    from
        ep.v_manu m
        
    inner join masterdata.manu mm
            on mm.id_ = trim (leading '0' from (substring (cast (m.manu_id as char(10)) from 3 for 15)))

    inner join masterdata.subsid s
            on s.oid = mm.clientele_oid 
        and s.subsid_txt2 = 'DE'
        and cast(mm.update_time as date) >= ?

    where m.prod_root_id = 'DE'

    order by
    mm.update_time desc;
    '''

    resultset = con.query(sql=sql, params=[date], columndescriptor=1) # needs formatting

    result = order_by_date(resultset)

    return result

def get_sup_data(date):
    sql = '''
    select
    su.sap_kreditor_no,
        su.supp_txt,
        su.prod_root_id,
        ssd.update_time
    from
        v_supp su
    
    inner join masterdata.suppl_subsid_data ssd
            on ssd.id_ = su.sap_kreditor_no
            and cast(ssd.update_time as date) >= ?
    
    inner join masterdata.subsid s
            on s.oid = ssd.clientele_oid 
        and s.subsid_txt2 = 'DE'
            
    where su.prod_root_id = 'DE'
    and su.supp_typ_id = 0
    and (su.sap_kreditor_no >= 740000 and su.sap_kreditor_no < 888888)
    and coalesce (regexp_substr (translate (su.supp_id using latin_to_unicode with error), '[A-Z]',1,1), '0') = '0' 
    and su.supp_id not in ('49100518', '49747700', '49100339', '49805041' ,'49375')

    order by
    ssd.update_time desc;
    '''

    resultset = con.query(sql=sql, params=[date], columndescriptor=1) # needs formatting

    result = order_by_date(resultset)

    return result

def order_by_date(rs):
    result = {}

    for row in rs:
        if row['update_time'].date() in result:
            result[row['update_time'].date()].append(row)
        else:
            result[row['update_time'].date()] = [row]
    return result