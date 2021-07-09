from fastapi import APIRouter, Depends
from fastapi.param_functions import Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from datetime import date

from dependencies import verify_token
from .db_connection import con
from .models import Manufacturer, Supplier, InternalProduct, Sellout

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

@router.get("/internalProducts", response_model=InternalProduct, summary="get internal products")
def get_internalProducts():
    '''
    Returns internal products.

    **Can't be tested in Swagger UI, because the response body is too large!**
    '''
    result = get_internalProducts_data()
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)

@router.get("/sellout/{contract_id}", response_model=Sellout, summary="get contract by id")
def get_selloutContract(contract_id: int = Path(None)):
    '''
    Returns contract information for given contract ID.
    '''
    result = get_selloutContract_data(contract_id)
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
             
    where ((ssd.id_ >= 740000 and ssd.id_ < 888888) or (ssd.id_ in (79922010,79922850)))
      and ssd.full_name is not null

    order by
    ssd.update_time desc;
    '''

    resultset = con.query(sql=sql, params=[date], columndescriptor=1) # needs formatting

    for row in resultset:
        row["prod_root_id"] = row["prod_root_id"].strip()

    #result = order_by_date(resultset)

    return resultset

def get_internalProducts_data():
    sql = '''
    select
        prod_org_id as id,
        prod_root_id as country,
        prod_txt as "name",
        manu_org_id as manufacturer,
        prod_grp_id as sub_category,
        upc_code_max as ean
    from ep.prod_all 
    where substring (cast (upc_code_max as char (13)) from 1 for 5) = '20000'
        and prod_root_id = 'DE'
    order by prod_org_id;
    '''
    
    resultset = con.query(sql=sql, columndescriptor=1)

    for row in resultset:
        row["country"] = row["country"].strip()
        row["ean"] = row["ean"].strip()

    return resultset

def get_selloutContract_data(contract_id):
    sql = '''
        select	
            distinct co.contract_id, 
            scf1.salesertrag, 
            vcf1.resertrag, 
            scf1.salesval, 
            vcf1.resval,
            case 
                when cfc.contract_id = co.contract_id then 1 
                else 0 
            end as abgerechnet
        from	gkm_so.condition co 
            left join (
                select	
                    contract_id, 
                    sum(cond_val) salesertrag, 
                    sum(sales_val) salesval 
                from	gkm_so.sales_condition_fulfilled 
                where	sellout_profit_flag = 1 
                    and cancelled_flag is null 
                group by 1) scf1
                on scf1.contract_id = co.contract_id 
            left join (
                select	
                    contract_id, 
                    sum(cond_val) resertrag, 
                    sum(voucher_val) resval 
                from	gkm_so.voucher_condition_fulfilled 
                where	sellout_profit_flag = 1 
                    and cancelled_flag is null 
                group by 1) vcf1
                on vcf1.contract_id = co.contract_id
            left join (
                select	
                    distinct contract_id 
                from	gkm_so.condition_final_claims) cfc
                    on co.contract_id = cfc.contract_id
        where	
            co.status <> 'S' 
            and co.mcond_id <> 0
            and co.contract_id = ?;
    '''
    resultset = con.query(sql=sql, params=[contract_id], columndescriptor=1)
    return resultset

def order_by_date(rs):
    result = {}

    for row in rs:
        if row['update_time'].date() in result:
            result[row['update_time'].date()].append(row)
        else:
            result[row['update_time'].date()] = [row]
    return result