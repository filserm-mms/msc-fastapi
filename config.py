from google.cloud import secretmanager
from google.cloud.secretmanager_v1.types.resources import ReplicationStatus

class Config():
    def __init__(self):

        self.PROJECT_ID = "mms-msc-msc-d-fx5e"

        client = secretmanager.SecretManagerServiceClient()
        secret = f"projects/{self.PROJECT_ID}/secrets/"
        version = "/versions/latest"
        
        # get api token
        response = client.access_secret_version(request={"name": secret + "msc-fast-api-token" + version})
        self.API_TOKEN = response.payload.data.decode("UTF-8")
        
        # get password
        response = client.access_secret_version(request={"name": secret + "msc-fast-api-password" + version})
        self.PASSWORD = response.payload.data.decode("UTF-8")

config = Config()
