import unittest

from core.format import CollectFormat


class MyCollectFormat1(CollectFormat):
    code = "my_collect_format"
    assoc_key = "resource_id"
    format_map = {
        "my_vm": {
            "resource_name": "resourceName",
            "resource_id": "${str(resourceId)}",
            "my_account": "${account_name}",  # 用于云主机关联账号
            "bk_inst_name": "${'%s-%s-%s'%(account_name,resourceId,resourceName)}",
        },
        "my_ds": {
            "resource_name": "resourceName",
            "resource_id": "${str(resourceId)}",
            "bk_inst_name": "${'%s-%s-%s'%(account_name,resourceId,resourceName)}",  # 用于云主机关联账号
            "my_vm": "${my_vm_map[str(vmId)]}",  # 用于云虚机关联
        },
    }


class TestCollectFormat(unittest.TestCase):
    def test_my_collect1(self):
        # 测试嵌套数据
        value = {
            "my_vm": [
                {
                    "resourceName": "vm-01",
                    "resourceId": 12345,
                },
                {
                    "resourceName": "vm-02",
                    "resourceId": 54321,
                },
            ],
            "my_ds": [
                {"resourceName": "ds-01", "resourceId": 100092, "vmId": 12345},
                {"resourceName": "ds-02", "resourceId": 100093, "vmId": 54321},
            ],
        }
        context = {
            "account_name": "测试云1",
        }
        mcf1 = MyCollectFormat1(value, context=context)
        result = mcf1.get()
        print(result)


if __name__ == "__main__":
    unittest.main()
