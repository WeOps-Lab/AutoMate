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
import abc
import ast
import copy
import re
from ast import NodeVisitor
from typing import List

from mako import codegen, lexer, parsetree
from mako.exceptions import MakoException
from mako.lexer import Lexer
from mako.template import Template

from core.logger import logger
from core.utils.sandbox import SANDBOX

TEMPLATE_PATTERN = re.compile(r"\${[^$#]+}")
RAW_LIST_PATTERN = r"\.(\d+)"
REPL_LIST_PATTERN = r"[\1]"
RAW_DICT_PATTERN = r"\.(\w+)"
REPL_DICT_PATTERN = r"['\1']"


class Null:
    pass


_ = Null()


def format_constant_key(key):
    """
    @summary: format key to ${key}
    @param key:
    @return:
    """
    return "${%s}" % key


def deformat_constant_key(key):
    """
    @summary: deformat ${key} to key
    @param key:
    @return:
    """
    return key[2:-1]


class ForbiddenMakoTemplateException(Exception):
    pass


class ConstantTypeException(Exception):
    pass


class MakoNodeCodeExtractor(object):
    @abc.abstractmethod
    def extract(self, node):
        """处理 Mako Lexer 分割出来的 code 对象，返回需要检测的 python 代码，返回 None 表示该节点不需要处理

        :param node: mako parsetree node
        :return: 需要处理的代码，或 None
        """
        raise NotImplementedError()


def parse_template_nodes(
    nodes: List[parsetree.Node],
    node_visitor: ast.NodeVisitor,
    code_extractor: MakoNodeCodeExtractor,
):
    """
    解析mako模板节点，逐个节点解析抽象语法树并检查安全性
    :param nodes: mako模板节点列表
    :param node_visitor: 节点访问类，用于遍历AST节点
    :param code_extractor: Mako 词法节点处理器，用于提取 python 代码
    """
    for node in nodes:
        code = code_extractor.extract(node)
        if code is None:
            continue

        ast_node = ast.parse(code, "<unknown>", "exec")
        node_visitor.visit(ast_node)
        if hasattr(node, "nodes"):
            parse_template_nodes(node.nodes, node_visitor)


def check_mako_template_safety(text: str, node_visitor: ast.NodeVisitor, code_extractor: MakoNodeCodeExtractor) -> bool:
    """
    检查mako模板是否安全，若不安全直接抛出异常，安全则返回True
    :param text: mako模板内容
    :param node_visitor: 节点访问器，用于遍历AST节点
    """
    try:
        lexer_template = Lexer(text).parse()
    except MakoException as mako_error:
        raise ForbiddenMakoTemplateException("非mako模板，解析失败, {err_msg}".format(err_msg=mako_error.__class__.__name__))
    parse_template_nodes(lexer_template.nodes, node_visitor, code_extractor)
    return True


class SingleLineNodeVisitor(NodeVisitor):
    """
    遍历语法树节点，遇到魔术方法使用或 import 时，抛出异常
    """

    def __init__(self, *args, **kwargs):
        super(SingleLineNodeVisitor, self).__init__(*args, **kwargs)

    def visit_Attribute(self, node):
        if node.attr.startswith("__"):
            raise ForbiddenMakoTemplateException("can not access private attribute")

    def visit_Name(self, node):
        if node.id.startswith("__"):
            raise ForbiddenMakoTemplateException("can not access private method")

    def visit_Import(self, node):
        raise ForbiddenMakoTemplateException("can not use import statement")

    def visit_ImportFrom(self, node):
        self.visit_Import(node)


class SingleLinCodeExtractor(MakoNodeCodeExtractor):
    def extract(self, node):
        if isinstance(node, parsetree.Code) or isinstance(node, parsetree.Expression):
            return node.text
        elif isinstance(node, parsetree.Text):
            return None
        else:
            raise ForbiddenMakoTemplateException("Unsupported node: [{}]".format(node.__class__.__name__))


class ConstantTemplate(object):
    def __init__(self, data):
        self.data = data

    def get_reference(self):
        reference = []
        templates = self.get_templates()
        for tpl in templates:
            reference += self.get_template_reference(tpl)
        reference = list(set(reference))
        return reference

    def get_templates(self):
        templates = []
        data = self.data
        if isinstance(data, str):
            templates += self.get_string_templates(data)
        if isinstance(data, (list, tuple)):
            for item in data:
                templates += ConstantTemplate(item).get_templates()
        if isinstance(data, dict):
            for value in list(data.values()):
                templates += ConstantTemplate(value).get_templates()
        return list(set(templates))

    def resolve_data(self, value_maps):
        data = self.data
        if isinstance(data, str):
            return self.resolve_string(data, value_maps)
        if isinstance(data, list):
            ldata = [""] * len(data)
            for index, item in enumerate(data):
                ldata[index] = ConstantTemplate(copy.deepcopy(item)).resolve_data(value_maps)
            return ldata
        if isinstance(data, tuple):
            ldata = [""] * len(data)
            for index, item in enumerate(data):
                ldata[index] = ConstantTemplate(copy.deepcopy(item)).resolve_data(value_maps)
            return tuple(ldata)
        if isinstance(data, dict):
            ddata = {}
            for key, value in list(data.items()):
                ddata[key] = ConstantTemplate(copy.deepcopy(value)).resolve_data(value_maps)
            return ddata
        return data

    @staticmethod
    def get_string_templates(string):
        return list(set(TEMPLATE_PATTERN.findall(string)))

    @staticmethod
    def get_template_reference(template):
        lex = lexer.Lexer(template)

        try:
            node = lex.parse()
        except MakoException as e:
            logger.warning("pipeline get template[{}] reference error[{}]".format(template, e))
            return []

        def compiler():
            return None

        compiler.reserved_names = set()
        identifiers = codegen._Identifiers(compiler, node)

        return list(identifiers.undeclared)

    @staticmethod
    def resolve_string(string, value_maps):
        if not isinstance(string, str):
            return string
        templates = ConstantTemplate.get_string_templates(string)

        if len(templates) == 1 and templates[0] == string and deformat_constant_key(string) in value_maps:
            return value_maps[deformat_constant_key(string)]

        for tpl in templates:

            try:
                check_mako_template_safety(tpl, SingleLineNodeVisitor(), SingleLinCodeExtractor())
            except ForbiddenMakoTemplateException as e:
                logger.warning("forbidden template: {}, exception: {}".format(tpl, e))
                continue
            except Exception:
                logger.exception("{} safety check error.".format(tpl))
                continue
            resolved = ConstantTemplate.resolve_template(tpl, value_maps)
            string = string.replace(tpl, resolved)
        return string

    @staticmethod
    def resolve_template(template, value_maps):
        data = {}
        data.update(SANDBOX)
        data.update(value_maps)
        if not isinstance(template, str):
            raise ConstantTypeException("constant resolve error, template[%s] is not a string" % template)
        try:
            tm = Template(template)
        except (MakoException, SyntaxError) as e:
            logger.error("resolve template[{}] error[{}]".format(template, e))
            return template
        try:
            resolved = tm.render_unicode(**data)
        except Exception as e:
            logger.warning("constant content({}) is invalid, data({}), error: {}".format(template, data, e))
            return template
        else:
            return resolved


def raw_to_mako(string):
    if not ConstantTemplate.get_string_templates(string):
        string = re.sub(RAW_LIST_PATTERN, REPL_LIST_PATTERN, string)
        string = re.sub(RAW_DICT_PATTERN, REPL_DICT_PATTERN, string)
        string = f"${{{string}}}"
    return string


def to_mako_repr(data):
    if isinstance(data, Null):
        return Null
    if isinstance(data, str):
        return raw_to_mako(data)
    if isinstance(data, list):
        ldata = [""] * len(data)
        for index, item in enumerate(data):
            ldata[index] = to_mako_repr(copy.deepcopy(item))
    if isinstance(data, tuple):
        ldata = [""] * len(data)
        for index, item in enumerate(data):
            ldata[index] = to_mako_repr(copy.deepcopy(item))
        return tuple(ldata)
    if isinstance(data, dict):
        ddata = {}
        for key, value in list(data.items()):
            ddata[key] = to_mako_repr(copy.deepcopy(value))
        return ddata
    return data
