from functools import lru_cache
import boto3
import botocore.credentials
import botocore.session
from boto3 import Session
from botocore.session import get_session


def create(access_key_id=None, access_key_secret=None, session_token=None, role_arn=None, role_external_id=None):
    return Client(
        get_credentials(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            session_token=session_token,
            role_arn=role_arn,
            role_external_id=role_external_id
        )
    )


def get_credentials(access_key_id=None, access_key_secret=None, session_token=None, role_arn=None,
                    role_external_id=None):
    credentials = None
    if access_key_id and access_key_secret:
        credentials = botocore.credentials.Credentials(access_key=access_key_id,
                                                       secret_key=access_key_secret,
                                                       token=session_token)
    if role_arn:
        credentials = _AssumeRoleCredentialsBuilder(role_arn, credentials, role_external_id=role_external_id).build()
    return credentials


class Client:
    def __init__(self, credentials=None):
        botocore_session = get_session()
        if credentials:
            botocore_session._credentials = credentials
        self.session = Session(botocore_session=botocore_session)

    @lru_cache(maxsize=20)
    def client(self, service_name, **kwargs):
        return self.session.client(service_name, **kwargs)

    @lru_cache(maxsize=20)
    def resource(self, service_name, **kwargs):
        return self.session.resource(service_name, **kwargs)

    def get(self, service_name, region=None, **kwargs):
        # For backwards compatibility
        if region is not None:
            kwargs["region_name"] = region
        return self.client(service_name, **kwargs)

class _AssumeRoleCredentialsBuilder:
    def __init__(self, role_arn, credentials, role_external_id=None, session_name='AssumeRoleUser',
                 duration_seconds=3600):
        if credentials:
            self.sts_client = boto3.client("sts", aws_access_key_id=credentials.access_key,
                                           aws_secret_access_key=credentials.secret_key,
                                           aws_session_token=credentials.token)
        else:
            self.sts_client = boto3.client("sts")

        self.role_arn = role_arn
        self.role_external_id = role_external_id
        self.session_name = session_name
        self.duration_seconds = duration_seconds

    def build(self):
        return botocore.credentials.RefreshableCredentials.create_from_metadata(
            metadata=self._refresh(),
            refresh_using=self._refresh,
            method="sts-assume-role",
        )

    def _refresh(self):
        params = {
            "RoleArn": self.role_arn,
            "RoleSessionName": self.session_name,
            "DurationSeconds": self.duration_seconds,
            "ExternalId": self.role_external_id,
        }
        response = self.sts_client.assume_role(**params).get("Credentials")
        expiration = response.get("Expiration").isoformat()
        return {
            "access_key": response.get("AccessKeyId"),
            "secret_key": response.get("SecretAccessKey"),
            "token": response.get("SessionToken"),
            "expiry_time": expiration
        }