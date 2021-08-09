from pydantic import BaseModel
from datetime import datetime
from typing import List

class Article(BaseModel):
    prod_id:        str
    country_d:      str
    prod_txt:       str
    manu_id:        str
    sub_category:   str
    ean:            str

    class Config:
        schema_extra = {
            "example": {
                "prod_id":      "2490314",
                "country_d":    "DE",
                "prod_txt":     "9407577 PS4 500GB BLACK",
                "manu_id":      "490000157",
                "sub_category": "3204",
                "ean":          "0711719407577",
            }
        }


class Manufacturer(BaseModel):
    manu_id:        str
    manu_txt:       str
    prod_root_id:   str
    update_time:    datetime

    class Config:
        schema_extra = {
            "example": {
                "manu_id":      "490006149",
                "manu_txt":     "CARSON",
                "prod_root_id": "DE",
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
    sap_kreditor_no:    str
    supp_txt:           str
    prod_root_id:       str
    update_time:        datetime

    class Config:
        schema_extra = {
            "example": {
                "sap_kreditor_no":  "823637",
                "supp_txt":         "MICHAEL HUBER/FABIAN FRISCHMANN - GBR DICHT & ERGREIFEND",
                "prod_root_id":     "DE",
                "update_time":      "2021-04-15T09:14:45.454000"
            }
        }

class InternalProduct(BaseModel):
    id:             str
    country:        str
    name:           str
    manufacturer:   str
    sub_category:   str
    ean:            str

    class Config:
        schema_extra = {
            "example": {
                "id": "1290300",
                "country": "DE",
                "name": "E+ MEIN BASE MIT HANDY 5 /GP 2010",
                "manufacturer": "893",
                "sub_category": "5092",
                "ean": "2000012903007"
            }
        }

class Sellout(BaseModel):
    gkm_vertragsnummer:     str
    summe_abverkaeufe:      float
    summe_reservierungen:   float
    ertrag_abverkaeufe:     float
    ertrag_reservierungen:  float
    abgerechnet:            str

    class Config:
        schema_extra = {
            "example": {
                "gkm_vertragsnummer": "605599",
                "summe_abverkaeufe": 4660,
                "summe_reservierungen": 590,
                "ertrag_abverkaeufe": 125510.8,
                "ertrag_reservierungen": 16773.34,
                "abgerechnet": "1"
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