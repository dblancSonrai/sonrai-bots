from functools import lru_cache
import sonrai.platform.aws.arn
import sonrai.platform.srn
from sonrai import context
from sonrai.platform.aws import client


class Context(context.Context):
    def __init__(self, config, bot, bcc):
        super().__init__(config, bot, bcc)

    def get_client(self, *args, account_id=None, **kwargs):
        if account_id is None:
            account_id = self._get_resource_id_account_id()
            if account_id is None:
                account_id = self._get_resource_srn_account_id()
        return self._create_client(**self._get_client_kwargs("aws", identifier=account_id))

    def _get_resource_id_account_id(self):
        resource_id = self.resource_id
        if not resource_id:
            return None
        return sonrai.platform.aws.arn.parse(resource_id).account_id

    def _get_resource_srn_account_id(self):
        resource_srn = self.resource_srn
        if not resource_srn:
            return None
        srn = sonrai.platform.srn.parse(resource_srn)
        if srn.cloud != 'aws':
            return None
        return srn.account

    @staticmethod
    @lru_cache(maxsize=20)
    def _create_client(**kwargs):
        return client.create(
            access_key_id=kwargs.get("access_key_id"),
            access_key_secret=kwargs.get("access_key_secret"),
            session_token=kwargs.get("session_token"),
            role_arn=kwargs.get("bot_role_arn"),
            role_external_id=kwargs.get("bot_role_external_id")
        )