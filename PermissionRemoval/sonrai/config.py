import pyhocon


def load(file_path):
    return Config(**pyhocon.ConfigFactory.parse_file(file_path))


class _ConfigDict(dict):
    def __init__(self, prefix, **kwargs):
        super().__init__(**kwargs)
        self._prefix = prefix

    def _get_required(self, key):
        v = self.get(key, None)
        if v is None:
            raise ValueError("Missing required value: {}.{}".format(self._prefix, key))
        return v


class Config(_ConfigDict):
    def __init__(self, **kwargs):
        super().__init__("", **kwargs)
        self['bot'] = _BotConfig("bot", **self._get_required("bot"))
        self['data'] = _DataConfig("data", **self._get_required("data"))
        self['content'] = _ContentConfig("content", **self._get_required("content"))
        self['aws'] = _AwsConfig("aws", **self.get("aws", {}))
        self['az'] = _AzureConfig("az", **self.get("az", {}))
        self['gcp'] = _GcpConfig("gcp", **self.get("gcp", {}))


class _BotConfig(_ConfigDict):
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)
        self['id'] = self._get_required('id')


class _DataConfig(_ConfigDict):
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)
        self['ticket'] = _TicketConfig("ticket", **self._get_required('ticket'))


class _TicketConfig(_ConfigDict):
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)


class _ContentConfig(_ConfigDict):
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)
        self['url'] = self._get_required('url')


class _AwsConfig(_ConfigDict):
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)
        clients = self.get('clients', None)
        if clients is None:
            clients = []
            self['clients'] = clients


class _AzureConfig(_ConfigDict):
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)


class _GcpConfig(_ConfigDict):
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)
