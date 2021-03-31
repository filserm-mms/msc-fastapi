# @Author: Michael Filser
# @Date:   2021-02-25 13:47:58

#pip install --upgrade google-cloud-bigquery

from google.cloud import bigquery
from google.oauth2 import service_account
import os

# to be implemented -> setting of environment variable outside of this module
os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS', 'C:/Users/filser/Documents/gcp-keys/mms-msc-msc-d-fx5e-8fc077b71c80.json')
key_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)


class BigQuery():

    def __init__(self):
        self.bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

    def __repr__(self):
        return f'BigQuery class'

    def query(self, sql, fmt=0):
        try:
            query_job = self.bq_client.query(sql)
            resultset=query_job.result()    #https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.table.RowIterator.html
            if fmt == 'pd':                 #pd = pandas
                resultset = resultset.to_dataframe()
            else:
                resultset = list(resultset)
        except Exception as error:
            raise Exception({error})
        else:
            return resultset


if __name__ == '__main__':
    con = BigQuery()
    print (con)
    sql = 'SELECT * FROM `mms-msc-msc-d-fx5e.msc_test.outlet_small` where outlet_id in (44,466)'
    resultset = con.query(sql)
    for row in resultset:
        for k, v in row.items():
            print ("key:", k, "value:", v)


