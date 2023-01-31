import random
import string


def get_random_pw(length=10):
    words = string.ascii_lowercase + string.ascii_uppercase + string.digits
    chosen = random.sample(words, length)
    return "".join(chosen)


def underline2hump(ul_str: str):
    """下划线转为驼峰"""
    return ul_str.title().replace("_", "")
