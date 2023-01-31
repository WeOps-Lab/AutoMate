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
import json
import re
from functools import partial

from django.utils.translation import ugettext_lazy as _
from gcloud.conf import settings

__group_name__ = _("自动化服务(Automate)")

from gcloud.utils.handlers import handle_api_error
from pipeline.component_framework.component import Component
from pipeline.core.flow.activity import Service
from pipeline.core.flow.io import StringItemSchema

VERSION = "1.0"

cc_handle_api_error = partial(handle_api_error, __group_name__)

get_client_by_user = settings.ESB_GET_CLIENT_BY_USER


class FormatTableService(Service):
    def inputs_format(self):
        return [
            self.InputItem(
                name=_("表格数据"),
                key="input_data",
                type="string",
                schema=StringItemSchema(description=_("表格数据")),
                required=True,
            ),
            self.InputItem(
                name=_("转换格式"),
                key="format_string",
                type="string",
                schema=StringItemSchema(description=_("转换格式")),
            ),
            self.InputItem(
                name=_("分隔符"),
                key="sep",
                type="string",
                schema=StringItemSchema(description=_("分隔符")),
            ),
        ]

    def outputs_format(self):
        return [
            self.OutputItem(
                name=_("转换后结果"), key="output_data", type="string", schema=StringItemSchema(description=_("表格数据"))
            )
        ]

    def execute(self, data, parent_data):
        input_data = data.inputs.input_data
        format_string = data.inputs.format_string
        sep = data.inputs.sep

        try:
            input_data = json.loads(input_data.replace("'", '"'))
        except Exception:
            data.outputs.ex_data = f"format_table input_data load error:input_data:{input_data}"
            return False
        input_list = []
        sub_regex = r"\{\{loop_items\.(.+?)\}\}"

        for _index, _input_data in enumerate(input_data):

            def replace_key(match):
                result = input_data[_index].get(match.group(1), "")
                return str(result)

            result = re.sub(sub_regex, replace_key, format_string)
            input_list.append(result.replace('"', ""))

        data.outputs.output_data = sep.join(input_list)
        return True


class FormatTableComponent(Component):
    name = _("表格转换脚本")
    version = VERSION
    code = "format_table"
    bound_service = FormatTableService
    embedded_form = True  # 内嵌式表单声明
    # 表单定义
    form = """ 
    (function(){
        $.atoms.format_table2 = [
        {
            "type": "input",
            "attrs": {
                "name": gettext("表格数据"),
                "hookable": true,
                "placeholder": gettext("表格数据")
            },
            "events": [],
            "methods": {},
            "tag_code": "input_data"
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("转换格式"),
                "hookable": true,
                "placeholder": gettext("转换格式,可使用{{loop_items.}} 使用表格里数据进行循环")
            },
            "events": [],
            "methods": {},
            "tag_code": "format_string"
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("分隔符"),
                "hookable": true,
                "placeholder": gettext("分隔符,如换行符,`-`等")
            },
            "events": [],
            "methods": {},
            "tag_code": "sep"
        },
    ]
    })();
    """
    desc = _(
        "1. 主要是把定义的表格数据(即ansible任务中循环遍历数据)转换为字符串\n"
        "2. format_string可直接使用循环变量,使用方式为{{loop_items.dict_key}},如{{loop_items.a}}"
    )
