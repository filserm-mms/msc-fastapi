from fastapi import FastAPI, Depends, APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
#from routers import contract_master, articles 
from routers import contract_master
from config import config
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

 # yaml
from fastapi.responses import Response, PlainTextResponse
import yaml, io, functools

app = FastAPI(docs_url='/api/docs',openapi_url="/api/openapi.json")
app.include_router(contract_master.router,prefix="/api")
#app.include_router(articles.router,prefix="/api")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/api", tags=["general"])
def read_root():
    return {"key": "value"}

@app.post("/api/token", tags=["general"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "msc" and form_data.password == config.PASSWORD:
        return {"access_token": config.API_TOKEN, "token_type": "bearer"}
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
    openapi_schema["info"]["contact"] = {
            "name":"Lukas, Gruber; Michael Filser; Moritz Schmidl", 
            "email":"margin.sellout.calculation@mediamarktsaturn.com",
            "url":"https://confluence.media-saturn.com/x/aCVyB"
            }
    openapi_schema["info"]["x-business-domain"] = "Condition Managment"
    openapi_schema["info"]["x-business-objects"] = ["test1", "test2"]
    openapi_schema["info"]["x-product"] = "Sellout Data"


    # override 422 status code -> this is necessary to fulfill the zally linter
    # https://github.com/tiangolo/fastapi/issues/2455
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if openapi_schema["paths"][path][method]["responses"].get("422"):
                openapi_schema["paths"][path][method]["responses"][
                    "400"
                ] = openapi_schema["paths"][path][method]["responses"]["422"]
                openapi_schema["paths"][path][method]["responses"].pop("422")


    app.openapi_schema = openapi_schema
    return app.openapi_schema

# additional yaml version of openapi.json
@app.get('/openapi.yaml', include_in_schema=False)
@functools.lru_cache()
def read_openapi_yaml() -> Response:
    openapi_json= app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type='text/yaml')

 
app.openapi = custom_openapi
