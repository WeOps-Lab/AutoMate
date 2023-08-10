# -*- coding: UTF-8 -*-


class ApplyParams(object):
    # 私有云控制台IP
    host = "host"
    host_aliyun = "region"
    host_vmware = "host"
    host_qcloud = "region"
    host_openstack = "host"
    host_huaweicloud = "region"
    host_fusioncompute = "host"

    # 登录账号
    account = "account"
    account_aliyun = "accesskey"
    account_vmware = "account"
    account_qcloud = "accesskey"
    account_openstack = "account"
    account_huaweicloud = "ak"
    account_fusioncompute = "account"

    # 登录账号密码
    password = "password"
    password_aliyun = "accessvalue"
    password_vmware = "password"
    password_qcloud = "accessvalue"
    password_openstack = "password"
    password_huaweicloud = "sk"
    password_fusioncompute = "password"

    # cpu规格
    cpu = "cpu"
    cpu_aliyun = "cpu"
    cpu_vmware = "cpu"
    cpu_qcloud = "cpu"
    cpu_openstack = "cpu"
    cpu_huaweicloud = "cpu"
    cpu_fusioncompute = "cpu"

    # 内存规格
    mem = "mem"
    mem_aliyun = "mem"
    mem_vmware = "mem"
    mem_qcloud = "mem"
    mem_openstack = "mem"
    mem_huaweicloud = "mem"
    mem_fusioncompute = "memory"

    # 主机名
    host_name = "host_name"
    host_name_aliyun = "InstanceName"
    host_name_vmware = "computer_name"
    host_name_qcloud = "InstanceName"
    host_name_openstack = "name"
    host_name_huaweicloud = "name"
    host_name_fusioncompute = "hostname"

    # 虚拟机密码
    vm_pwd = "vm_pwd"
    vm_pwd_aliyun = "Password"
    vm_pwd_vmware = "vmtemplate_pwd"
    vm_pwd_qcloud = "Password"
    vm_pwd_openstack = "admin_pass"
    vm_pwd_huaweicloud = "adminPass"
    vm_pwd_fusioncompute = "passwd"

    # 计算资源
    spec_name = "spec_name"
    spec_name_aliyun = "spec_name"
    spec_name_vmware = "spec_name"
    spec_name_qcloud = "spec_name"
    spec_name_openstack = "spec_name"
    spec_name_huaweicloud = "spec_name"

    # 数据盘列表
    disk = "disk"
    disk_aliyun = "disk"
    disk_vmware = "disk"
    disk_qcloud = "disk"
    disk_openstack = "disk"
    disk_huaweicloud = "disk"
    disk_fusioncompute = "disk_info"

    # 数据盘类型
    disk_type = "disk_type"
    disk_type_aliyun = "Category"
    disk_type_vmware = "disk_type"
    disk_type_qcloud = "DiskType"
    disk_type_openstack = "disk_type"
    disk_type_huaweicloud = "disk_type"

    # 数据盘大小
    disk_size = "disk_size"
    disk_size_aliyun = "Size"
    disk_size_vmware = "disk_size"
    disk_size_qcloud = "DiskSize"
    disk_size_openstack = "size"
    disk_size_huaweicloud = "disk_size"

    # 子网掩码
    mask = "mask"
    mask_vmware = "mask"
    mask_fusioncompute = "mask"

    # 网关
    gateway = "gateway"
    gateway_vmware = "gateway"
    gateway_fusioncompute = "gateway"

    # DNS
    dns = "dns"
    dns_vmware = "dns"
    dns_fusioncompute = "dns"

    # 操作系统
    os = "os"
    os_vmware = "vmtemplate_os"
    os_fusioncompute = "osType"

    # 镜像
    image = "image"
    image_aliyun = "imageId"
    image_vmware = "vmtemplate_moId"
    image_qcloud = "ImageId"
    image_openstack = "image_id"
    image_huaweicloud = "imageRef"
    image_fusioncompute = "template_id"

    # datacenter id
    dc_moId = "dc_moId"
    dc_moId_vmware = "dc_moId"

    # 集群 id
    hc_moId = "hc_moId"
    hc_moId_vmware = "hc_moId"
    hc_moId_fusioncompute = "location"

    # 存储 id
    ds_moId = "ds_moId"
    ds_moId_vmware = "ds_moId"
    ds_moId_fusioncompute = "datastore"

    # vpc
    vpc = "vpc"
    vpc_qcloud = "VpcId"
    vpc_openstack = "net-id"
    vpc_huaweicloud = "vpcid"

    # switch id
    vswitch_id = "vswitch_id"
    vswitch_id_aliyun = "VSwitchId"
    vswitch_id_vmware = "vs_moId"
    vswitch_id_qcloud = "SubnetId"
    vswitch_id_openstack = "subnet_id"
    vswitch_id_huaweicloud = "subnet_id"
    vswitch_id_fusioncompute = "vswitch_id"

    # 端口组
    port_group_fusioncompute = "portGroupUrn"

    # 文件夹 id
    folder_moId = "folder_moId"
    folder_moId_vmware = "folder_moId"
    folder_moId_fusioncompute = "parentObjUrn"

    # 公有云规格
    instance_type = "instance_type"
    instance_type_aliyun = "InstanceType"
    instance_type_qcloud = "InstanceType"
    instance_type_openstack = "flavor_id"
    instance_type_huaweicloud = "flavorRef"

    # 安全组
    securitygroup = "securitygroup"
    securitygroup_aliyun = "SecurityGroupId"
    securitygroup_qcloud = "SecurityGroupIds"
    securitygroup_openstack = "security_groups"
    securitygroup_huaweicloud = "security_groups"

    # 区域
    region = "region"
    region_aliyun = "regionId"
    region_qcloud = "Region"
    region_openstack = "region_name"

    # 可用区
    zone = "zone"
    zone_aliyun = "ZoneId"
    zone_qcloud = "Zone"
    zone_openstack = "availability_zone"
    zone_huaweicloud = "availability_zone"
    site_fusioncompute = "site"

    # 付费类型
    pay_type = "pay_type"
    pay_type_aliyun = "InstanceChargeType"
    pay_type_qcloud = "InstanceChargeType"
    pay_type_huaweicloud = "InstanceChargeType"

    # 付费周期
    period = "period"
    period_aliyun = "Period"
    period_qcloud = "Period"
    period_huaweicloud = "periodNum"

    # 项目id
    project_id = "project_id"
    project_id_openstack = "project_id"
    project_id_huaweicloud = "project_id"

    # 虚拟机IP
    ip = "ip"
    ip_vmware = "ip"
    ip_aliyun = "PrivateIpAddress"
    ip_qcloud = "PrivateIpAddresses"
    ip_openstack = "ip"
    ip_huaweicloud = "ip_address"
    ip_fusioncompute = "ip"

    # 账号IP
    domain_id = "domain_id"
    domain_id_huaweicloud = "domain_id"
