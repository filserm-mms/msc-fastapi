from pydantic import BaseModel
from datetime import datetime
from typing import List

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

""" class ManufacturerList(BaseModel):
    date: List[Manufacturer]

    class Config:
        schema_extra = {
            "example": {
                "2021-03-09": [
                        Manufacturer.Config.schema_extra["example"]
                ]
            }
        }

 """
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

""" 
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
 """