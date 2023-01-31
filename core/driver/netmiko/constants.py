# -- coding: utf-8 --

# @File : constants.py
# @Time : 2022/10/19 10:25
# @Author : windyzhao

DEVICE_TYPE_BASE_PROMPT = {
    "cisco_ios": r"{0}\#$|{0}\(config.*\)\#$|{0}\>$",
    "cisco_ios_telnet": r"{0}\#$|{0}\(config.*\)\#$|{0}\>$",
    "hp_comware": r"\<{0}(\-.*)?\>$|\[{0}(\-.*)?\]$",
    "hp_comware_telnet": r"\<{0}(\-.*)?\>$|\[{0}(\-.*)?\]$",
    "huawei": r"\<{0}(\-.*)?\>$|\[{0}(\-.*)?\]$",
    "huawei_telnet": r"\<{0}(\-.*)?\>$|\[{0}(\-.*)?\]$",
}
