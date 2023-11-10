from core.driver.cmp.collect import CMPCollectFormat


class TemplateCloudFormat(CMPCollectFormat):
    code = "cmp_collect_templatecloud"
    type = "cmp_collect"
    tag = "cmp.collect.templatecloud"
    name = "XX云数据转换(cmp)"
    desc = "XX云数据转换(cmp)"
    format_map = {
        "resource_name": "resource_name",
        "resource_id": "resource_id",
        "inner_ip.0": "ip_addr",
        "public_ip.0": "public_ip",
        "region": "region",
        "zone": "zone",
        "vpc": "vpc",
        "status": "status",
        "instance_type": "instance_type",
        "os_name": "os_name",
        "vcpus": "vcpus",
        "memory": "memory_mb",
        "bk_obj_id": "bk_obj_id",
        "task_id": "task_id",
        "bk_inst_name": "templatecloud_account",  # 用于云主机关联账号
        "charge_type": "charge_type",
        "create_time": "create_time",
        "expired_time": "expired_time",
    }
