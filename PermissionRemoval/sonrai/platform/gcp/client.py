from google.oauth2 import service_account
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def create(service_account_credentials_path=None):
    return Client(service_account_credentials_path=service_account_credentials_path)


class Client:

    def __init__(self, service_account_credentials_path=None):
        if service_account_credentials_path is not None:
            self.get_client = service_account.Credentials.from_service_account_file(filename=service_account_credentials_path,
                                                         scopes=['https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/bigquery','https://www.googleapis.com/auth/datastore','https://www.googleapis.com/auth/pubsub','https://www.googleapis.com/auth/devstorage.full_control'])
        else:
            self.get_client = GoogleCredentials.get_application_default()

    def get(self, client, version):
        return discovery.build(client, version, credentials=self.get_client, cache_discovery=False)
