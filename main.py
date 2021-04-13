from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from routers import articles

app = FastAPI()

app.include_router(articles.router)

@app.get("/")
def read_root():
    return {"key": "value"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "msc" and form_data.password == "123":
        return {"access_token": "1234asdf", "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")