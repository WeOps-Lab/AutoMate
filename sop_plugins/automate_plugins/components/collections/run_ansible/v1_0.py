# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import copy
import json
import re
from functools import partial

import requests
from bamboo_engine.utils.boolrule import BoolRule
from django.utils.translation import ugettext_lazy as _
from gcloud.conf import settings

__group_name__ = _("自动化服务(Automate)")

from gcloud.utils.handlers import handle_api_error
from pipeline.component_framework.component import Component
from pipeline.core.flow.activity import Service
from pipeline.core.flow.io import ArrayItemSchema, BooleanItemSchema, ObjectItemSchema, StringItemSchema

VERSION = "1.0"

cc_handle_api_error = partial(handle_api_error, __group_name__)

get_client_by_user = settings.ESB_GET_CLIENT_BY_USER


class RunAnsibleService(Service):
    def inputs_format(self):
        return [
            self.InputItem(
                name=_("接入点"),
                key="access_point",
                type="string",
                schema=StringItemSchema(description=_("接入点")),
                required=True,
            ),
            self.InputItem(
                name=_("模块名"), key="module", type="string", schema=StringItemSchema(description=_("模块名")), required=True
            ),
            self.InputItem(
                name=_("模块参数"),
                key="module_args",
                type="string",
                schema=StringItemSchema(description=_("模块参数")),
            ),
            self.InputItem(
                name=_("是否循环"),
                key="is_loop",
                type="bool",
                schema=StringItemSchema(description=_("如果循环,则在模块参数使用变量[i]")),
                required=True,
            ),
            self.InputItem(
                name=_("循环变量"),
                key="loop_items",
                type="string",
                schema=StringItemSchema(description=_("循环变量")),
            ),
            self.InputItem(
                name=_("凭据key"),
                key="credential_id",
                type="string",
                schema=StringItemSchema(description=_("凭据key")),
                required=True,
            ),
            self.InputItem(
                name=_("Ansible请求成功条件"),
                key="run_ansible_success_exp",
                type="string",
                schema=StringItemSchema(
                    description=_("根据返回的 JSON 的数据来控制节点的成功或失败, " "使用 resp 引用返回的 JSON 对象，例 resp.data.result.change==True")
                ),
            ),
            self.InputItem(
                name=_("失败信息层级"),
                key="run_ansible_error_message_exp",
                type="string",
                schema=StringItemSchema(description=_("失败信息层级, " "使用 resp 引用返回的 JSON 对象，例 resp.data.message")),
            ),
        ]

    def outputs_format(self):
        return [
            self.OutputItem(
                name=_("成功的数据行"),
                key="success_loop_items",
                type="string",
                schema=StringItemSchema(description=_("成功的数据行")),
            ),
            self.OutputItem(
                name=_("失败数据行"),
                key="failed_loop_items",
                type="string",
                schema=StringItemSchema(description=_("失败数据行")),
            ),
            self.OutputItem(
                name=_("是否全部失败"),
                key="is_all_failed",
                type="bool",
                schema=StringItemSchema(description=_("是否全部失败")),
            ),
            self.OutputItem(
                name=_("Ansible结果"),
                key="ansible_results",
                type="array",
                schema=ArrayItemSchema(
                    description=_("Ansible结果列表"),
                    item_schema=ObjectItemSchema(
                        description=_("每条记录结果"),
                        property_schemas={
                            "index": StringItemSchema(description=_("记录索引")),
                            "result": BooleanItemSchema(description=_("是否成功")),
                            "message": StringItemSchema(description=_("响应结果")),
                            "data": StringItemSchema(description=_("响应数据")),
                        },
                    ),
                ),
            ),
        ]

    def execute(self, data, parent_data):
        self.logger.info(f"data:{data},parent_data:{parent_data}")
        module = data.inputs.module
        module_args = data.inputs.module_args
        credential_id = data.inputs.credential_id
        if credential_id:
            credential_id = credential_id.strip('"').strip("'")
        is_loop = data.inputs.is_loop
        loop_items = data.inputs.loop_items

        run_ansible_success_exp = data.inputs.run_ansible_success_exp
        run_ansible_error_message_exp = data.inputs.run_ansible_error_message_exp
        message_level = run_ansible_error_message_exp.split(".")
        if message_level and message_level[0] != "resp":
            data.outputs.ex_data = (
                f"run_ansible_error_message_exp error:run_ansible_error_message_exp:{run_ansible_error_message_exp}"
            )
            return False
        message_level = message_level[1:]

        loop_items = data.inputs.loop_items
        if is_loop:
            try:
                loop_items = json.loads(loop_items.replace("'", '"'))
            except Exception:
                self.logger.exception("loop_items load error")
                data.outputs.ex_data = f"loop_items load error:loop_items:{loop_items}"
                return False
            module_args_list = []
            sub_regex = r"\{\{loop_items\.(.+?)\}\}"

            for _index, loop_item in enumerate(loop_items):

                def replace_key(match):
                    result = loop_items[_index].get(match.group(1), "")
                    return str(result)

                module_args_list.append(re.sub(sub_regex, replace_key, module_args))
        else:
            module_args_list = [module_args]
        self.logger.info(f"module_args_list:{module_args_list}")
        url = f"{data.inputs.access_point}/api/ansible/v1/fast_execute_adhoc"
        error = False
        ansible_results = []
        success_loop_items = []
        failed_loop_items = []

        def get_message(result, level):
            result = copy.deepcopy(result)
            if not isinstance(result, dict):
                self.logger.warn(
                    f"get_error_message warning result level is not dict" f"[result:{result},level:{level}"
                )
                return {}
            result = result.get(level, {})
            return result

        for _index, _module_args in enumerate(module_args_list):
            post_data = dict(module=module, module_args=_module_args, credential_id=credential_id)
            try:
                resp = requests.post(url=url, json=post_data, verify=False)
                result = resp.json()
            except Exception as e:
                self.logger.error(f"post ansible request error:{repr(e)}")
                ansible_result = {
                    "index": _index,
                    "result": False,
                    "message": "post ansible request error:[automate service error]",
                    "data": "{}",
                }
                if is_loop:
                    failed_loop_items.append(loop_items[_index])
                ansible_results.append(ansible_result)
                error = True
                continue
            self.logger.info(f"post ansible request error:url:{url}, data: {post_data},result:{result}")

            if not result["result"]:
                error = True
                self.logger.error(
                    f"post ansible request error:module:{module},"
                    f"module_args:{_module_args}result:{result['result']},"
                    f"message:{result['message']}"
                )
                ansible_result = {
                    "index": _index,
                    "result": result["result"],
                    "message": result["message"],
                    "data": "{}",
                }
                if is_loop:
                    failed_loop_items.append(loop_items[_index])
                ansible_results.append(ansible_result)
                continue

            if run_ansible_success_exp:
                try:
                    rule = BoolRule(run_ansible_success_exp)
                    if not rule.test(context={"resp": result}):
                        if is_loop:
                            failed_loop_items.append(loop_items[_index])

                        error_message = ""
                        data_result = result
                        for level in message_level:
                            error_message = data_result = get_message(data_result, level)

                        ansible_result = {
                            "index": _index,
                            "result": False,
                            "message": f"错误信息:{error_message or ''}",
                            "data": "{}",
                        }
                        ansible_results.append(ansible_result)
                        continue
                except Exception as e:
                    err = _("请求成功条件判定出错: {}")
                    self.logger.error(err.format(repr(e)))
                    if is_loop:
                        failed_loop_items.append(loop_items[_index])
                    error_message = ""
                    data_result = result
                    for level in message_level:
                        error_message = data_result = get_message(data_result, level)
                    ansible_result = {
                        "index": _index,
                        "result": False,
                        "message": f"错误信息:{error_message or ''}",
                        "data": "{}",
                    }
                    ansible_results.append(ansible_result)
                    continue
            ansible_result = {
                "index": _index,
                "result": result,
                "message": result["message"],
                "data": json.dumps(result["data"]),
            }
            ansible_results.append(ansible_result)
            if is_loop:
                success_loop_items.append(loop_items[_index])

        data.outputs.ansible_results = ansible_results
        data.outputs.success_loop_items = json.dumps(success_loop_items)
        data.outputs.failed_loop_items = json.dumps(failed_loop_items)
        # 如果为非批量,则取出ansible记录第一条的结果作为成功和失败的方式
        data.outputs.is_all_failed = not bool(success_loop_items) if is_loop else not ansible_results[0]["result"]
        if error or (not is_loop and not ansible_results[0]["result"]):
            data.outputs.ex_data = "\n".join(
                [f"{i['index'] + 1}:{i['message']}" for i in filter(lambda x: not x["result"], ansible_results)]
            )
            return False
        return True


class RunAnsibleComponent(Component):
    name = _("执行ansible脚本")
    version = VERSION
    code = "run_ansible"
    bound_service = RunAnsibleService
    embedded_form = True  # 内嵌式表单声明
    # 表单定义
    form = """ 
    (function(){
        $.atoms.run_ansible = [
        {
            "type": "input",
            "attrs": {
                "name": gettext("接入点"),
                "hookable": true,
                "placeholder": gettext("接入点,如http://127.0.0.1:8000")
            },
            "events": [],
            "methods": {},
            "tag_code": "access_point"
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("模型名"),
                "hookable": true,
                "placeholder": gettext("模型名,如ping")
            },
            "events": [],
            "methods": {},
            "tag_code": "module"
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("模型参数"),
                "hookable": true,
                "placeholder": gettext("模型参数,多个参数,空格分隔")
            },
            "events": [],
            "methods": {},
            "tag_code": "module_args"
        },
        {
            "tag_code": "is_loop",
            "type": "radio",
            "attrs": {
                "name": gettext("是否循环"),
                "hookable": true,
                "items": [
                    {"value": true, "name": gettext("是")},
                    {"value": false,"name": gettext("否")}
                ],
                "default": true,
                "validation": [
                    {
                        "type": "required"
                    }
                ]
            }
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("循环变量"),
                "hookable": true,
                "placeholder": gettext("模型参数,多个参数,空格分隔")
            },
            "events": [],
            "methods": {},
            "tag_code": "loop_items"
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("凭据key"),
                "hookable": true,
                "placeholder": gettext("凭据key,/xx/xx")
            },
            "events": [],
            "methods": {},
            "tag_code": "credential_id"
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("Ansible请求成功条件"),
                "hookable": true,
                "placeholder": gettext("根据返回的 JSON 的数据来控制节点的成功或失败, \" \"使用 resp 引用返回的 JSON 对象，例 resp.result==True")
            },
            "events": [],
            "methods": {},
            "tag_code": "run_ansible_success_exp"
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("失败信息层级"),
                "hookable": true,
                "placeholder": gettext("失败信息层级 ,使用 resp 引用返回的 JSON 对象，例 resp.result.message")
            },
            "events": [],
            "methods": {},
            "tag_code": "run_ansible_error_message_exp"
        }
    
    ]
    })();
    """
    desc = _(
        '1. 如果需要循环,循环变量为[{"a":1,"b":2},{"a":3,"b":4}]\n'
        "2. module_args可直接使用循环变量,使用方式为{{loop_items.dict_key}},如{{loop_items.a}}\n"
        "3. 返回的成功和失败数据行即为循环变量内的数据,可传递给下个节点."
    )
