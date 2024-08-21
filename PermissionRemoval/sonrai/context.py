import json

from sonrai.graphql.client import GraphQLClient
from sonrai.graphql.token import ManagedBotGraphQLToken


def create(config, bot, bcc):
    cloud = bot.cloud
    if cloud == "aws":
        from sonrai.platform.aws.context import Context
        return Context(config, bot, bcc)
    elif cloud == "azure":
        from sonrai.platform.azure.context import Context
        return Context(config, bot, bcc)
    elif cloud == "gcp":
        from sonrai.platform.gcp.context import Context
        return Context(config, bot, bcc)
    elif cloud == "any":
        from sonrai.context import Context
        return Context(config, bot, bcc)
    raise ValueError("Unsupported bot cloud: {}".format(cloud))


class Context:
    def __init__(self, config, bot, bcc):
        self.config = config
        self.resource_srn = config.get('data').get('ticket').get('resourceSRN')
        self.resource_id = config.get('data').get('ticket').get('criticalResourceID')
        self.bot = bot
        self._bcc = bcc
        self._graphql_client = None

    def graphql_client(self):
        if self._graphql_client is None:
            token = ManagedBotGraphQLToken(self.config.get('bot').get('id'), self.config.get('job').get('id'), self._bcc)
            self._graphql_client = GraphQLClient(token)
        return self._graphql_client

    def get_client(self):
        raise NotImplementedError()

    def _get_client_kwargs(self, cloud, identifier=None):
        c = self.config.get(cloud)
        client_kwargs = None
        if c:
            clients = c.get("clients")
            if clients:
                if identifier is not None and identifier in clients:
                    client_kwargs = clients[identifier]
                else:
                    client_kwargs = clients.get("default")
        return client_kwargs if client_kwargs is not None else {}

    def get_policy_evidence(self):
        v = self.config.get('data')
        if v:
            v = v.get("ticket")
            if v:
                v = v.get("evidence")
                if v:
                    v = v.get("policyEvidence")
                    if v:
                        try:
                            return json.loads(v)
                        except TypeError:
                            return v

        return None

    def get_policy_evidence_data(self):
        v = self.get_policy_evidence()
        if v is not None:
            return v.get("data")

        return None

