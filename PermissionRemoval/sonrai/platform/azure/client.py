import json

import requests
from .cred_wrapper import CredentialWrapper
from azure.common.client_factory import get_client_from_json_dict
from azure.identity import DefaultAzureCredential, ClientSecretCredential

class Client:
    def __init__(self, tenant_id=None, client_id=None, client_secret=None, audience=None):
        self.tenant_id = tenant_id
        if not tenant_id or not client_id or not client_secret:
            credential = DefaultAzureCredential()
        else:
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        audience = audience or "https://management.azure.com/.default"
        # To support authentication with Azure SDK libraries that have not been updated to accept
        # the core credential objects, we wrap the credential in a backwards compatibility layer
        self.credential = CredentialWrapper(credential, audience=audience)
        self.credentials = self.credential # Alias for self.credential
        self.config_dict = {
            "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
            "resourceManagerEndpointUrl": "https://management.azure.com/",
            "activeDirectoryGraphResourceId": "https://graph.windows.net/",
            "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
            "galleryEndpointUrl": "https://gallery.azure.com/",
            "managementEndpointUrl": "https://management.core.windows.net/"
        }

    def get(self, client, tenant_id=None, credentials=None, **kwargs):
        """
        This method will return an instance of the provided `client` class.
        :param client: The class to instantiate. Must conform to the Azure core SDK scheme, meaning
            at a minimum, it will accept a `credentials` argument.
        :param tenant_id: An alternative tenant_id to be used with the client.
            The tenant_id set for this Client object is used by default.
        :param credentials: Alternative credentials to be used with the client.
            The credentials set for this Client object are used by default.
        :param kwargs: Any additional arguments to provide to the constructor such as `subscription_id`
        :type tenant_id: str
        :type credentials: :class:`azure.core.credentials.TokenCredential`
        :type kwargs: dict
        :return:
        """
        credentials = credentials if credentials is not None else self.credentials
        tenant_id = tenant_id if tenant_id is not None else self.tenant_id
        config_dict = self.config_dict.copy()
        config_dict["tenantId"] = tenant_id
        # Some older clients may accept 'credential' instead of 'credentials', populate both
        return get_client_from_json_dict(client, config_dict, credential=credentials, credentials=credentials, **kwargs)


class ManagedIdentityClient:
    def __init__(self, credentials, tenant_id, *_, **__):
        self.credentials = credentials
        self.tenant_id = tenant_id

    def delete(self, object_path):
        url = "https://management.azure.com/{}".format(object_path)
        params = {'api-version': '2015-08-31-preview'}
        _rest(url, self.credentials, params=params, method_type='delete')


def _rest(url, credentials, scopes=None, params=None, data=None, method_type='get'):
    scopes = scopes if scopes is not None else ("https://management.azure.com",)
    token = credentials.get_token(*scopes).token
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    with requests.request(str(method_type).upper(), headers=headers, url=url, data=json.dumps(data), params=params) as response:
        response.raise_for_status()
