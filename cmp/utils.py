# 统一管理CMP的Utils


def convert_param_to_list(param):
    """
    将传入的未定格式的参数转换成列表
    Args:
        param (all): 未确定类型参数

    Returns:

    """
    if not param and param != 0:
        return []
    if not isinstance(param, (str, list, int)):
        raise Exception("传入参数不为空时，类型仅支持str和list。请修改！")
    return param if isinstance(param, list) else [param]
