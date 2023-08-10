from core.format import CredentialFormat, format_util
from core.utils.vault import HvacManager


class CMPCredentialFormat(CredentialFormat):
    code = "cmp_credential_base"
    type = "cmp_collect"
    tag = "cmp.collect"
    name = "凭据转换(cmp)"
    desc = "凭据转换(cmp)"
    format_map = {}


def get_cmp_cred_by_path(cloud_type: str, path: str, context=None) -> str:
    """根据凭据ID获取凭据数据"""
    secret = HvacManager().read_secret(path)
    credential = format_util.format_cmp_credential(cloud_type, secret, context=context)
    return credential
