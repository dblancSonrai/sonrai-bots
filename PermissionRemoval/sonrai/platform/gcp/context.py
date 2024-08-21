from functools import lru_cache
from sonrai import context
from sonrai.platform.gcp import client

class Context(context.Context):
    def __init__(self, config, bot, bcc):
        super().__init__(config, bot, bcc)

    def get_client(self, *args, **kwargs):
        return self._create_client(**self._get_client_kwargs("gcp"))

    @staticmethod
    @lru_cache(maxsize=20)
    def _create_client(**kwargs):
        return client.create(
            service_account_credentials_path=kwargs.get('service_account_path')
        )