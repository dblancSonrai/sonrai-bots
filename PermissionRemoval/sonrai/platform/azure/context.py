from functools import lru_cache
from sonrai import context
from sonrai.platform.azure.client import Client

class Context(context.Context):
    def __init__(self, config, bot, bcc):
        super().__init__(config, bot, bcc)

    def get_client(self, *args, audience=None, **kwargs):
        return self._create_client(audience=audience, **self._get_client_kwargs("azure"))

    @staticmethod
    @lru_cache(maxsize=20)
    def _create_client(tenant_id=None, client_id=None,
                       client_secret=None, audience=None):
        return Client(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            audience=audience
        )