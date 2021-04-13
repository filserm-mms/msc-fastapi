from fastapi import APIRouter, Depends
from fastapi.param_functions import Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from dependencies import verify_token
from .db_connection import con

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    dependencies=[Depends(verify_token)]
)

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


@router.get("/prod_id/{prod_id}", response_model=Article, summary="get a single article")
def get_prod_id(prod_id: int = Path(...)):
    result = get_data(prod_id=prod_id, delete_mark=-1)
    json_compatible_item_data = jsonable_encoder(result)
    return JSONResponse(content=json_compatible_item_data)


@router.get("/get_all_articles_germany/{delete_mark}", response_model=Article, summary="get a list of articles - input parameter: delete mark")
def get_all_articles_germany(delete_mark: int = Path(...),):
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
    