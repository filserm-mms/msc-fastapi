from fastapi import APIRouter, Depends
from fastapi.param_functions import Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from datetime import date

from dependencies import verify_token
from .db_connection import con
from .models import Manufacturer, Supplier

router = APIRouter(
    prefix="/contractMaster",
    tags=["contractMaster"],
    dependencies=[Depends(verify_token)]
)

@router.get("/manu/{date}", response_model=Manufacturer, summary="get manufacturers by date")
def get_manufacturers(date: date = Path(None)):
    '''
    **{date}** has to be in the format of **"YYYY-MM-DD"**

    Returns all manufacturers which have been updated since {date}.
    '''
    result = get_manu_data(date)
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)

@router.get("/supplier/{date}", response_model=Supplier, summary="get suppliers by date")
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
        mm.id_ + 490000000 as manu_id,
        mm.name_ as manu_txt,
        s.subsid_txt2 as prod_root_id,
        mm.update_time
    from
        masterdata.manu mm

    inner join masterdata.subsid s
            on s.oid = mm.clientele_oid 
        and s.subsid_txt2 = 'DE'
        and cast(mm.update_time as date) >= ?

    order by
    mm.update_time desc;
    '''

    resultset = con.query(sql=sql, params=[date], columndescriptor=1) # needs formatting

    for row in resultset:
        row["prod_root_id"] = row["prod_root_id"].strip()

    #result = order_by_date(resultset)

    return resultset

def get_sup_data(date):
    sql = '''
    select
        ssd.id_ as sap_kreditor_no,
        ssd.full_name as supp_txt,
        s.subsid_txt2 as prod_root_id,
        ssd.update_time
    from
        masterdata.suppl_subsid_data ssd
       
    inner join masterdata.subsid s
            on s.oid = ssd.clientele_oid 
           and s.subsid_txt2 = 'DE'
           and cast(ssd.update_time as date) >= ?
             
    where (ssd.id_ >= 740000 and ssd.id_ < 888888)
      and ssd.full_name is not null

    order by
    ssd.update_time desc;
    '''

    resultset = con.query(sql=sql, params=[date], columndescriptor=1) # needs formatting

    for row in resultset:
        row["prod_root_id"] = row["prod_root_id"].strip()

    #result = order_by_date(resultset)

    return resultset

def order_by_date(rs):
    result = {}

    for row in rs:
        if row['update_time'].date() in result:
            result[row['update_time'].date()].append(row)
        else:
            result[row['update_time'].date()] = [row]
    return result