# -- coding: utf-8 --
from core.driver.cmp.credential import CMPCredentialFormat


class TemplateCredentialFormat(CMPCredentialFormat):
    code = "cmp_credential_template"
    type = "cmp_credential"
    tag = "cmp.credential.template"
    name = "XX云凭据转换(cmp)"
    desc = "XX云凭据转换(cmp)"
    format_map = {"account": "access_key", "password": "access_secret"}
