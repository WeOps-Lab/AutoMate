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

from django.utils.translation import ugettext_lazy as _
from gcloud.conf import settings

__group_name__ = _("自动化服务(Automate)")

from pipeline.component_framework.component import Component
from pipeline.core.flow.activity import Service
from pipeline.core.flow.io import StringItemSchema

VERSION = "1.0"


class TableRespService(Service):
    def inputs_format(self):
        return [
            self.InputItem(
                name=_("总表格数据"),
                key="table_loop_items",
                type="string",
                schema=StringItemSchema(description=_("总表格数据,如${loop_items}")),
                required=True,
            ),
            self.InputItem(
                name=_("最终成功数据"),
                key="table_success_loop_items",
                type="string",
                schema=StringItemSchema(description=_("最终成功数据,如${success_items}")),
            ),
            self.InputItem(
                name=_("返回格式"),
                key="resp_format",
                type="string",
                schema=StringItemSchema(description=_("成功返回格式,默认为全数据,可使用 {{loop_items.key}} 或者 ${}")),
            ),
        ]

    def execute(self, data, parent_data):
        table_loop_items = data.inputs.table_loop_items
        table_success_loop_items = data.inputs.table_success_loop_items
        resp_format = data.inputs.resp_format

        try:
            table_loop_items = json.loads(table_loop_items.replace("'", '"'))
        except Exception:
            data.outputs.ex_data = f"table_loop_items input_data load error:table_loop_items:{table_loop_items}"
            return False
        try:
            table_success_loop_items = json.loads(table_success_loop_items.replace("'", '"'))
        except Exception:
            data.outputs.ex_data = (
                f"table_success_loop_items input_data load error:table_success_loop_items:{table_success_loop_items}"
            )
            return False
        table_failed_loop_items = [i for i in table_loop_items if i not in table_success_loop_items]
        if not table_failed_loop_items:
            return True
        if not table_success_loop_items:
            data.outputs.ex_data = "全部失败"
            return False

        def get_resp(input_data, sep="，"):
            resp_list = []
            sub_regex = r"\{\{loop_items\.(.+?)\}\}"

            for _index, _input_data in enumerate(input_data):

                def replace_key(match):
                    result = input_data[_index].get(match.group(1), "")
                    return str(result)

                result = re.sub(sub_regex, replace_key, resp_format)
                resp_list.append(result.replace('"', ""))

            return sep.join(resp_list)

        success_resp = get_resp(table_success_loop_items)
        failed_resp = get_resp(table_failed_loop_items)
        data.outputs.ex_data = (
            "部分成功；"
            f"成功{len(table_success_loop_items)}个："
            f"{success_resp}；"
            f"失败{len(table_failed_loop_items)}个："
            f"{failed_resp}；"
        )
        return False


class TableRespComponent(Component):
    name = _("表格返回脚本")
    version = VERSION
    code = "table_resp"
    bound_service = TableRespService
    embedded_form = True  # 内嵌式表单声明
    # 表单定义
    form = """
    (function(){
        $.atoms.table_resp = [
        {
            "type": "input",
            "attrs": {
                "name": gettext("总表格数据"),
                "hookable": true,
                "placeholder": gettext("总表格数据,如${loop_items}")
            },
            "events": [],
            "methods": {},
            "tag_code": "table_loop_items"
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("最终成功数据"),
                "hookable": true,
                "placeholder": gettext("最终成功数据,如${success_items}")
            },
            "events": [],
            "methods": {},
            "tag_code": "table_success_loop_items"
        },
        {
            "type": "input",
            "attrs": {
                "name": gettext("返回格式"),
                "hookable": true,
                "placeholder": gettext("成功返回格式,默认为全数据,可使用 {{loop_items.key}} 或者 ${}")
            },
            "events": [],
            "methods": {},
            "tag_code": "resp_format"
        },
    ]
    })();
"""
    desc = _(
        "1. 主要是把定义的表格数据(即ansible任务中循环遍历数据)成功失败结果显示"
        "2. resp_format可直接使用循环变量,使用方式为{{loop_items.dict_key}},如{{loop_items.a}}"
    )
