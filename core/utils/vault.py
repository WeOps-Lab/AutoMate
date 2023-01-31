import hvac

from core.exception.base import CredentialNotFound
from core.logger import logger
from core.settings import settings


class HvacManager(object):
    def __init__(self):
        self.client = hvac.Client(url=settings.vault_url, token=settings.vault_token)

    def read_secret(self, path):
        try:
            result = self.client.secrets.kv.v2.read_secret(path)
        except Exception as e:
            logger.exception(f"[vault read secret error] path:{path},error:{repr(e)}")
            raise CredentialNotFound()
        secret = result.get("data", {}).get("data")
        if not secret:
            logger.warning(f"[vault read secret error] path:{path},result:{result}")
            raise CredentialNotFound()
        return secret
