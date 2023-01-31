import typing

import six


def clean_items(
    items: typing.Union[typing.Dict, typing.List[typing.Dict]],
    filter_map: typing.Dict,
    context: typing.Union[typing.Dict, None] = None,
    iterable_flatten: bool = True,
) -> typing.Union[typing.Dict, typing.List[typing.Dict]]:
    """
    根据filter_map清洗数据
    :param items: dict or list
    :param filter_map: 字段映射
    :param iterable_flatten: 是否打平可迭代对象
    :return:

    example:
    >>> clean_items([{"a":1,"b":{"c":2,"d":3}},{"a":3,"b":{"c":6,"d":7}}],{"a":"aa","b.d":"bd"})
    [{'aa': 1, 'bd': 3}, {'aa': 3, 'bd': 7}]
    >>> clean_items({"a":1,"b":{"c":2,"d":3}},{"a":"aa","b.d":"bd"})
    {'aa': 1, 'bd': 3}
    """
    new_items = {}
    if isinstance(items, dict):
        new_items = clean_data(items, filter_map=filter_map, context=context, iterable_flatten=iterable_flatten)
    elif isinstance(items, list):
        new_items = [
            clean_data(i, filter_map=filter_map, context=context, iterable_flatten=iterable_flatten) for i in items
        ]

    return new_items


def clean_data(
    data: typing.Dict,
    filter_map: typing.Dict,
    context: typing.Union[typing.Dict, None] = None,
    iterable_flatten: bool = True,
) -> typing.Dict:
    # 数据打平
    result = {}
    data = flatten(data, iterable_flatten=iterable_flatten)
    for field, filter_value in filter_map.items():
        if callable(filter_value):
            value = filter_value(data, context)
            result[field] = value
            continue
        elif isinstance(filter_value, list):
            value = "-".join(str(data.get(i) or context.get(i) or "") for i in filter_value)
            result[field] = value
            continue
        elif isinstance(filter_value, str):
            value = data.get(field) or context.get(field) or ""
            result[filter_value] = value
    return result


def _construct_key(previous_key, separator, new_key, replace_separators=None):
    """
    Returns the new_key if no previous key exists, otherwise concatenates
    previous key, separator, and new_key
    :param previous_key:
    :param separator:
    :param new_key:
    :param str replace_separators: Replace separators within keys
    :return: a string if previous_key exists and simply passes through the
    new_key otherwise
    """
    if replace_separators is not None:
        new_key = str(new_key).replace(separator, replace_separators)
    if previous_key:
        return f"{previous_key}{separator}{new_key}"
    else:
        return new_key


def flatten(nested_dict, separator=".", root_keys_to_ignore=None, replace_separators=None, iterable_flatten=True):
    """
    Flattens a dictionary with nested structure to a dictionary with no
    hierarchy
    Consider ignoring keys that you are not interested in to prevent
    unnecessary processing
    This is specially true for very deep objects
    :param nested_dict: dictionary we want to flatten
    :param separator: string to separate dictionary keys by
    :param root_keys_to_ignore: set of root keys to ignore from flattening
    :param str replace_separators: Replace separators within keys
    :return: flattened dictionary
    """
    assert isinstance(nested_dict, dict), "flatten requires a dictionary input"
    assert isinstance(separator, six.string_types), "separator must be string"

    if root_keys_to_ignore is None:
        root_keys_to_ignore = set()

    if len(nested_dict) == 0:
        return {}

    # This global dictionary stores the flattened keys and values and is
    # ultimately returned
    flattened_dict = dict()

    def _flatten(object_, key, iterable_flatten=True):
        """
        For dict, list and set objects_ calls itself on the elements and for
        other types assigns the object_ to
        the corresponding key in the global flattened_dict
        :param object_: object to flatten
        :param key: carries the concatenated key for the object_
        :return: None
        """
        # Empty object can't be iterated, take as is
        if not object_:
            flattened_dict[key] = object_
        # These object types support iteration
        elif isinstance(object_, dict):
            for object_key in object_:
                if not (not key and object_key in root_keys_to_ignore):
                    _flatten(
                        object_[object_key],
                        _construct_key(key, separator, object_key, replace_separators=replace_separators),
                        iterable_flatten=iterable_flatten,
                    )
        elif iterable_flatten and isinstance(object_, (list, set, tuple)):
            for index, item in enumerate(object_):
                _flatten(
                    item,
                    _construct_key(key, separator, index, replace_separators=replace_separators),
                    iterable_flatten=iterable_flatten,
                )
        # Anything left take as is
        else:
            flattened_dict[key] = object_

    _flatten(nested_dict, None, iterable_flatten=iterable_flatten)
    return flattened_dict


if __name__ == "__main__":
    # items = [{"a":1,"b":{"c":2,"d":3}},{"a":3,"b":{"c":6,"d":7}}]
    items = {"a": 1, "b": {"c": 2, "d": 3}}
    filter_map = {"a": "aa", "b.d": "bd"}
    print(clean_items(items, filter_map))
