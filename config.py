from google.cloud import secretmanager
import os

class Config():
    def __init__(self):
        self.PASSWORD = os.getenv("PASSWORD", None)
        self.API_TOKEN = os.getenv("API_TOKEN", None)

        if(not self.PASSWORD or not self.API_TOKEN):
            # TBD: does not work in docker container
            PROJECT_ID = "mms-msc-msc-d-fx5e"

            client = secretmanager.SecretManagerServiceClient()
            secret = f"projects/{PROJECT_ID}/secrets/"
            version = "/versions/latest"
            
            # get api token
            response = client.access_secret_version(request={"name": secret + "msc-fast-api-token" + version})
            self.API_TOKEN = response.payload.data.decode("UTF-8")
            
            # get password
            response = client.access_secret_version(request={"name": secret + "msc-fast-api-password" + version})
            self.PASSWORD = response.payload.data.decode("UTF-8")


config = Config()
