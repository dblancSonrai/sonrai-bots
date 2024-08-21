import jwt
import time
import logging


class _BotGraphQLToken:
    _ENV_KEY = 'https://sonraisecurity.com/env'
    _ORG_KEY = 'https://sonraisecurity.com/org'
    _GRAPHQL_URL_FMT = 'https://{}{}.sonraisecurity.com/graphql'
    _EXPIRY_THRESHOLD_SEC = 0

    def __init__(self, bot_id, job_id, bcc):
        self._bot_id = bot_id
        self._job_id = job_id
        self._bcc = bcc
        self._value = None

    def expired(self):
        now = time.time()
        remaining = self._exp - now
        logging.info("Token expires in: {}".format(remaining))
        return remaining < self._EXPIRY_THRESHOLD_SEC

    def get_graphql_url(self):
        if self._value is None:
            self.get()
        env = self._env
        org = self._org
        if not env:
            raise ValueError("No env present in token")
        if not org:
            raise ValueError("No org present in token")
        # e.g https://devtenant.de.sonraisecurity.com/graphql
        if env == 'dev':
            env_sub = '.de'
        # e.g https://stagetenant.s.sonraisecurity.com/graphql
        elif env == 'stage':
            env_sub = '.s'
        # e.g https://prodtenant.sonraisecurity.com/graphql
        elif env == 'crc':
            env_sub = ''
        else:
            raise ValueError("Unsupported env: {}".format(env))
        return self._GRAPHQL_URL_FMT.format(org, env_sub)

    def _set(self, value):
        if not value:
            raise ValueError("No token specified")
        decoded = jwt.decode(value,
                             options={"verify_signature": False})
        self._value = value
        self._org = decoded.get(self._ORG_KEY, None)
        self._env = decoded.get(self._ENV_KEY, None)
        self._exp = int(decoded.get('exp', 0))

    def get(self):
        if self._value is None:
            self._refresh(True)
        else:
            self._refresh()
        return self._value

    def _refresh(self, force=False):
        raise NotImplementedError()


class ManagedBotGraphQLToken(_BotGraphQLToken):
    _EXPIRY_THRESHOLD_SEC = 5 * 60  # 5 minutes

    def __init__(self, bot_id, job_id, bcc):
        super().__init__(bot_id, job_id, bcc)

    def _refresh(self, force=False):
        if force or self.expired():
            token = self._bcc.get_graphql_token(self._bot_id, self._job_id)
            self._set(token)
            logging.info("API token expires: " + str(self._exp))
