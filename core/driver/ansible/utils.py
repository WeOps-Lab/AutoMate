import typing


def parse_dict_to_args(_dict: typing.Dict):
    return " ".join(
        ["=".join((key, f'"{value}"' if isinstance(value, str) else str(value))) for key, value in _dict.items()]
    )
