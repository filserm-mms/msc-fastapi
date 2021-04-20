from fastapi import FastAPI, Depends, APIRouter
from fastapi.exceptions import HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from routers import articles, contract_master
from dependencies import API_TOKEN
from routers import contract_master, articles 

""" # yaml
from fastapi.responses import Response
import yaml, io, functools """

app = FastAPI(docs_url='/api/docs',openapi_url="/api/openapi.json")
app.include_router(contract_master.router,prefix="/api")
app.include_router(articles.router,prefix="/api")

@app.get("/api", tags=["general"])
def read_root():
    return {"key": "value"}

@app.post("/api/token", tags=["general"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "msc" and form_data.password == "E=<6+:jGPrg_SYT~":
        return {"access_token": API_TOKEN, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

# OpenAPI spec
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="MSC API",
        version="0.1.0",
        description="This is the API of Margin and Sellout Calculation!",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

""" # additional yaml version of openapi.json
@app.get('/openapi.yaml', include_in_schema=False)
@functools.lru_cache()
def read_openapi_yaml() -> Response:
    openapi_json= app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type='text/yaml')

 """
app.openapi = custom_openapi
