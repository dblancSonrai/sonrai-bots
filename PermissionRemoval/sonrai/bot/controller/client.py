import hashlib
import logging
import os
import tarfile
import tempfile
import traceback

import requests

from sonrai.bot import Bot

logger = logging.getLogger()

def from_url(url):
    from urllib.parse import urlsplit
    scheme, netloc, path, query, fragment = urlsplit(url)
    if scheme == 'local':
        return _LocalBotControllerClient(path)
    return BotControllerClient(url)

class BotControllerClient:
    _TIMEOUT = (10, 30) # connect_timeout, read_timeout

    def __init__(self, url, temp_dir=tempfile.tempdir):
        if not url:
            raise ValueError("url is required")
        if not url.endswith("/"):
            url = url + "/"
        self._url = url
        self._temp_dir = temp_dir

    def write_bot_action(self, bot_id, data=None, exc_info=None):
        body = { "botId": bot_id }
        if data:
            body["data"] = data
        if exc_info:
            e_type, exception, tb = exc_info
            body["failure"] = {
                "message": str(exception),
                "stack_trace": "".join(traceback.format_exception(e_type, exception, tb))
            }
            url = self._url + "v1/bots/action/remediation/apply/failure"
        else:
            url = self._url + "v1/bots/action/remediation/apply/success"
        with requests.post(url, timeout=self._TIMEOUT, json=body) as r:
            r.raise_for_status()
            try:
                action_srn = r.json().get("actionSrn")
            except Exception as e:
                logger.warning("Failed to retrieve actionSrn from response: {}".format(e))
                action_srn = None
            logger.info("Submitted bot action: {}".format(action_srn))


    def download_bot(self, bot_id, d, **kwargs):
        self._download_and_unpack_blob(bot_id, d, **kwargs)
        return Bot.from_dir(d)

    def _download_and_unpack_blob(self, bot_id, d, **kwargs):
        if not os.path.exists(d):
            os.makedirs(d)
        elif not os.path.isdir(d):
            raise ValueError("File is not a directory: " + d)
        f = self._download_blob(bot_id, **kwargs)
        try:
            with tarfile.open(f, "r:gz") as fp:
                fp.extractall(d)
        finally:
            os.remove(f)

    def _download_blob(self, bot_id, f=None, chunk_size=16384):
        with requests.get(self._url + "v1/bots/blob", stream=True, timeout=self._TIMEOUT, params={"botId": bot_id}) as r:
            r.raise_for_status()
            expect_hash = r.headers.get("Content-Hash")
            expect_hash = expect_hash.lower().strip() if expect_hash else None
            h = hashlib.sha256() if expect_hash else None
            if f is None:
                fpi, f = tempfile.mkstemp(prefix="blob", suffix=".tar.gz", dir=self._temp_dir)
                fp = os.fdopen(fpi, 'wb')
            else:
                fp = open(f, 'wb')
            with fp:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if h is not None:
                        h.update(chunk)
                    fp.write(chunk)
                if h is not None:
                    actual_hash = h.hexdigest().lower().strip()
                    if expect_hash != actual_hash:
                        raise IOError("Expected hash is not equal to actual hash: {} != {}".format(expect_hash, actual_hash))
        return f

    def get_graphql_token(self, bot_id, job_id):
        body = { "botId": bot_id, "jobId": job_id }
        with requests.get(self._url + "v1/bots/graphql/token", timeout=self._TIMEOUT, params=body) as r:
            r.raise_for_status()
            try:
                access_token = r.json()["token"]["access_token"]
                if not access_token:
                    raise ValueError("Access Token is empty")
                return access_token
            except Exception as e:
                raise ValueError("Failed to retrieve access token: {}".format(e))

class _LocalBotControllerClient:
    def __init__(self, path, **__):
        if not path:
            raise ValueError("Path is empty")
        elif not os.path.exists(path):
            raise ValueError("Invalid path: " + path + ". File path does not exist")
        elif os.path.isdir(path):
            path = os.path.join(path, "manifest.yaml")
        if not os.path.isfile(path):
            raise ValueError("Invalid path: " + path + ". Does not point to valid manifest file")
        self._dir = os.path.dirname(path)

    def download_bot(self, *_, **__):
        return Bot.from_dir(self._dir)

    def write_bot_action(self, bot_id, data=None, exc_info=None):
        pass

    def get_graphql_token(self, bot_id, job_id):
        try:
            with open('/tmp/sonrai/token') as token_source:
                my_token = token_source.read().strip()
            return my_token
        finally:
            pass

