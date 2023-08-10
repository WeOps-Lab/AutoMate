import unittest

from core.format import MakoFormat
from core.utils.mako_utils import _

status_enum = {"1": "running", "0": "stop", "-1": "deprecated"}


class MyMakoFormat1(MakoFormat):
    code = "my_mako1"
    format_map = {
        "resource_name": "resourceName",
        "resource_id": "${str(resourceId)}",
        "inner_ip": "resourceIp.0",
        "region": "${str(regionId)}",
        "status": "${status_enum[str(status)]}",
        "os_name": "${osType.replace('-','_')}",
        "vcpus": "${str(vcpus)}",
        "memory_mb": "${int(memoryKb)//1024}",
        "bk_obj_id": "bk_obj_id",  # 用于context传入
        "task_id": "task_id",  # 用于context传入
        "bk_inst_name": "${'%s-%s-%s'%(account_inst,resourceId,resourceName)}",  # 用于云主机关联账号
        "create_time": "${createTime[:19]}",
        "expired_time": "${expiredTime[:19]}",
    }


class MyMakoFormat2(MakoFormat):
    code = "my_mako2"
    format_map = {
        "my_vm": {
            "resource_name": "resourceName",
            "resource_id": "${str(resourceId)}",
            "inner_ip": "resourceIp.0",
            "region": "${str(regionId)}",
            "status": "${status_enum[str(status)]}",
            "os_name": "${osType.replace('-','_')}",
            "vcpus": "${str(vcpus)}",
            "memory_mb": "${int(memoryKb)//1024}",
            "bk_obj_id": "${vm_obj}",  # 用于context传入
            "task_id": "task_id",  # 用于context传入
            "bk_inst_name": "${'%s-%s-%s'%(account_inst,resourceId,resourceName)}",  # 用于云主机关联账号
            "create_time": "${createTime[:19]}",
            "expired_time": "${expiredTime[:19]}",
        },
        "my_ds": {
            "resource_name": "resourceName",
            "resource_id": "${str(resourceId)}",
            "region": "${str(regionId)}",
            "disk_total": "${diskTotal//1024}",
            "bk_obj_id": "${ds_obj}",  # 用于context传入
            "task_id": "task_id",  # 用于context传入
            "bk_inst_name": "${'%s-%s-%s'%(account_inst,resourceId,resourceName)}",  # 用于云主机关联账号
            "create_time": "${createTime[:19]}",
            "expired_time": "${expiredTime[:19]}",
        },
    }


class MyMakoFormat3(MakoFormat):
    code = "my_mako3"
    format_map = {"attr": _, "attr2": _}

    def get_attr(self, item, **kwargs):
        return item["pp_attr"]

    def get_attr2(self, item, context, **kwargs):
        return context["attr2_prefix"] + item["pp_attr2"]


class MyMakoFormat4(MakoFormat):
    code = "my_mako4"
    format_map = {"my_vm": {"attr1": _}, "my_ds": {"attr2": _}}

    def get_my_vm_attr1(self, item, **kwargs):
        return item["pp_attr"]

    def get_my_ds_attr2(self, item, context, **kwargs):
        return context["attr2_prefix"] + item["pp_attr2"]


class MyMakoFormat5(MakoFormat):
    code = "my_mako5"
    format_map = {}

    def get(self):
        result = super().get()
        result.update({"hello": "world"})
        return result


class TestMyMakoFormat(unittest.TestCase):
    def test_my_mako1(self):
        value = [
            {
                "resourceName": "vm-01",
                "resourceId": 12345,
                "resourceIp": ["1.1.1.1", "2.2.2.2"],
                "regionId": 12,
                "status": 0,
                "osType": "CentOs-7.6",
                "vcpus": "16",
                "memoryKb": 4194304,
                "createTime": "2022-10-10 12:10:23T123456",
                "expiredTime": "2023-10-10 12:10:23T345678",
            },
            {
                "resourceName": "vm-02",
                "resourceId": 54321,
                "resourceIp": ["3.1.1.1", "4.2.2.2"],
                "regionId": 22,
                "status": 1,
                "osType": "Redhat",
                "memoryKb": 12582912,
                "vcpus": "8",
                "createTime": "2022-10-12 12:10:23T123456",
                "expiredTime": "2023-10-20 12:10:23T345678",
            },
        ]
        context = {
            "account_inst": "测试云1",
            "status_enum": status_enum,
            "bk_obj_id": "my_vm",
            "task_id": "1qaz2wsx3edc4rfv",
        }
        mmf = MyMakoFormat1(value, context=context)
        result = mmf.get()
        print(result)
        assert result[0]["resource_name"] == "vm-01"
        assert isinstance(result[0]["resource_id"], str)
        assert result[0]["inner_ip"] == "1.1.1.1"
        assert result[0]["status"] == "stop"
        assert result[1]["status"] == "running"
        assert result[0]["os_name"] == "CentOs_7.6"
        assert result[0]["create_time"] == "2022-10-10 12:10:23"
        assert result[0]["bk_inst_name"] == "测试云1-12345-vm-01"
        assert result[0]["memory_mb"] == "4096"

        print(result)

    def test_my_mako2(self):
        # 测试嵌套数据
        value = {
            "my_vm": [
                {
                    "resourceName": "vm-01",
                    "resourceId": 12345,
                    "resourceIp": ["1.1.1.1", "2.2.2.2"],
                    "regionId": 12,
                    "status": 0,
                    "osType": "CentOs-7.6",
                    "vcpus": "16",
                    "memoryKb": 4194304,
                    "createTime": "2022-10-10 12:10:23T123456",
                    "expiredTime": "2023-10-10 12:10:23T345678",
                },
                {
                    "resourceName": "vm-02",
                    "resourceId": 54321,
                    "resourceIp": ["3.1.1.1", "4.2.2.2"],
                    "regionId": 22,
                    "status": 1,
                    "osType": "Redhat",
                    "memoryKb": 12582912,
                    "vcpus": "8",
                    "createTime": "2022-10-12 12:10:23T123456",
                    "expiredTime": "2023-10-20 12:10:23T345678",
                },
            ],
            "my_ds": [
                {
                    "resourceName": "ds-01",
                    "resourceId": 100092,
                    "regionId": 12,
                    "vcpus": "16",
                    "diskTotal": 4194304,
                    "createTime": "2022-10-10 12:10:23T123456",
                    "expiredTime": "2023-10-10 12:10:23T345678",
                },
                {
                    "resourceName": "ds-02",
                    "resourceId": 100093,
                    "regionId": 12,
                    "vcpus": "16",
                    "diskTotal": 8388608,
                    "createTime": "2022-10-10 12:10:23T123456",
                    "expiredTime": "2023-10-10 12:10:23T345678",
                },
            ],
        }
        context = {
            "account_inst": "测试云1",
            "status_enum": status_enum,
            "bk_obj_id": "my_vm",
            "task_id": "1qaz2wsx3edc4rfv",
            "vm_obj": "my_vm",
            "ds_obj": "my_ds",
        }
        mmf2 = MyMakoFormat2(value, context=context)
        result = mmf2.get()
        print(result)

    def test_my_mako3(self):
        """测试方法重写"""
        value = {"pp_attr": 12, "pp_attr2": "hello"}
        context = {"attr2_prefix": "attr2_"}
        mmf3 = MyMakoFormat3(value, context=context)
        result = mmf3.get()
        print(result)
        assert result["attr"] == 12
        assert result["attr2"] == "attr2_hello"

    def test_my_mako4(self):
        value = {"my_vm": [{"pp_attr": 11}, {"pp_attr": 22}], "my_ds": [{"pp_attr2": "hello"}, {"pp_attr2": "world"}]}
        context = {"attr2_prefix": "attr2_"}
        mmf4 = MyMakoFormat4(value, context=context)
        result = mmf4.get()
        print(result)
        assert result["my_vm"][0]["attr1"] == 11
        assert result["my_ds"][1]["attr2"] == "attr2_world"

    def test_my_mako5(self):
        mmf5 = MyMakoFormat5({})
        result = mmf5.get()
        assert result["hello"] == "world"


if __name__ == "__main__":
    unittest.main()
