# -*- coding: UTF-8 -*-
import functools

from .exceptions import RewriteException


def singleton(cls):
    _instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return get_instance


class CloudManageBase(object):
    """Cloud Manage Base class.

    The object defines multiple common methods for hybrid cloud.
    """

    # connection status
    def get_connection_result(self):
        """
        check if this object works.
        :return: A dict with a “key: value” pair of object. The key name is result, and the value is a boolean type.
        :rtype: dict
        """
        raise RewriteException()

    def list_regions(self, *args, **kwargs):
        """
        get region list on cloud platforms
        :rtype: dict
        """
        raise RewriteException()

    def list_zones(self, *args, **kwargs):
        """
        get zone list on cloud platforms
        :rtype: dict
        """
        raise RewriteException()

    def list_projects(self, *args, **kwargs):
        """
        get project list on cloud platforms
        :rtype: dict
        """
        raise RewriteException()

    def list_domains(self, *args, **kwargs):
        """
        get domain list on cloud platforms
        :rtype: dict
        """
        raise RewriteException()

    # ------------------***** compute *****-------------------
    def list_instance_types(self, *args, **kwargs):
        """
        get instance type list on cloud platforms
        :rtype: dict
        """
        raise RewriteException()

    def list_vms(self, *args, **kwargs):
        """
        Get vm list on cloud platforms
        :rtype: dict
        """
        raise RewriteException()

    def create_vm(self, *args, **kwargs):
        """
        Create a vm.
        :rtype: dict
        """
        raise RewriteException()

    def start_vm(self, vm_id, *args, **kwargs):
        """
        Start a vm.
        :param vm_id: vm id.
        :rtype: dict
        """
        raise RewriteException()

    def stop_vm(self, vm_id, *args, **kwargs):
        """
        Stop a vm.
        :param vm_id: vm id.
        :rtype: dict
        """
        raise RewriteException()

    def restart_vm(self, vm_id, *args, **kwargs):
        """
        Restart a vm.
        :param vm_id: vm id.
        :rtype: dict
        """
        raise RewriteException()

    def modify_vm(self, vm_id, *args, **kwargs):
        """
        Resize a vm.
        :param vm_id: vm id.
        :rtype: dict
        """
        raise RewriteException()

    def delete_vm(self, vm_id, *args, **kwargs):
        """
        Destroy a vm.
        :param vm_id: vm id.
        :rtype: dict
        """
        raise RewriteException()

    def list_available_specs(self, *args, **kwargs):
        """
        Get available specs.
        :rtype: dict
        """
        raise RewriteException()

    def add_vm_disk(self, *args, **kwargs):
        """
        Create a disk and attach to a specific vm.
        :rtype: dict
        """
        raise RewriteException()

    def remote_connect_vm(self, *args, **kwargs):
        """
        Connect to a remote vm desktop.
        :rtype: dict
        """
        raise RewriteException()

    def list_vm_disks(self, vm_id, *args, **kwargs):
        """
        Get all disks from a specific VM instance.
        :param vm_id: the ID of a specific vm.
        :rtype: dict
        """
        raise RewriteException()

    def instance_security_group_action(self, *args, **kwargs):
        """
        给实例绑定/解绑安全组
        :return:
        :rtype:
        """
        raise RewriteException()

    # ------------------***** snapshot *****------------------
    def create_snapshot(self, *args, **kwargs):
        """
        Create a snapshot of a given volume or vm.
        :rtype: dict
        """
        raise RewriteException()

    def delete_snapshot(self, snapshot_id, *args, **kwargs):
        """
        Delete a specific disk or vm snapshot.
        :param snapshot_id: snapshot id.
        :rtype: dict
        """
        raise RewriteException()

    def list_snapshots(self, *args, **kwargs):
        """
        Get snapshots from specified volume or vm.
        :rtype: dict
        """
        raise RewriteException()

    def restore_snapshot(self, *args, **kwargs):
        """
        Restore a specific vm or volume from a specific snapshot.
        :rtype: dict
        """
        raise RewriteException()

    # ------------------***** tag *****------------------
    def create_tag(self, *args, **kwargs):
        """
        Create a tag.
        :return:
        """
        raise RewriteException()

    def delete_tag(self, tag_id, *args, **kwargs):
        """
        Delete a tag.
        :return:
        """
        raise RewriteException()

    def update_tag(self, tag_id, *args, **kwargs):
        """
        Update key-value of a tag.
        :param tag_id: tag id.
        :rtype: dict
        """
        raise RewriteException()

    def list_tags(self, *args, **kwargs):
        """
        Get tag list on cloud platforms.
        :rtype: dict
        """
        raise RewriteException()

    def remove_resource_tag(self, *args, **kwargs):
        """
        Delete a specific tag from a specific resource.
        """
        raise RewriteException()

    def list_resource_tags(self, *args, **kwargs):
        """
        Get all tags from a specific resource.
        """
        raise RewriteException()

    # ------------------***** storage *****-------------------
    def list_disks(self, *args, **kwargs):
        """
        Get disk list on cloud platforms.
        :rtype: dict
        """
        raise RewriteException()

    def create_disk(self, *args, **kwargs):
        """
        Create a disk.
        :rtype: dict
        """
        raise RewriteException()

    def attach_disk(self, *args, **kwargs):
        """
        Attach a specific disk to a specific vm.
        :rtype: dict
        """
        raise RewriteException()

    def detach_disk(self, *args, **kwargs):
        """
        Detach a specific disk from a specific vm.
        :rtype: dict
        """
        raise RewriteException()

    def delete_disk(self, disk_id, *args, **kwargs):
        """
        Delete a specific disk
        :param disk_id: disk id.
        :rtype: dict
        """
        raise RewriteException()

    def extend_disk(self, disk_id, *args, **kwargs):
        """
        extend a specific disk
        :param disk_id: disk id.
        :rtype: dict
        """
        raise RewriteException()

    def list_images(self, *args, **kwargs):
        """
        Get image list.
        :rtype: dict
        """
        raise RewriteException()

    def delete_image(self, image_id, *args, **kwargs):
        """
        Delete a specific image.
        :param image_id: image id.
        :rtype: dict
        """
        raise RewriteException()

    # ------------------***** network *****-------------------
    def list_security_groups(self, *args, **kwargs):
        """
        Get security group list.
        :rtype: dict
        """
        raise RewriteException()

    def delete_security_group(self, security_group_id, *args, **kwargs):
        """
        Delete a specific security group.
        :param security_group_id: security group id.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        raise RewriteException()

    def create_security_group(self, *args, **kwargs):
        """
        Create a specific security group.
        :param kwargs: accept multiple key value pair arguments.
        :rtype: dict
        """
        raise RewriteException()

    def modify_security_group(self, security_group_id, *args, **kwargs):
        """
        Modify a specific security group.
        :param security_group_id: security group id(resource_id).
        :rtype: dict
        """
        raise RewriteException()

    def list_security_group_rules(self, *args, **kwargs):
        """
        Get a specific rule info from a specific security group.
        :rtype: dict
        """
        raise RewriteException()

    def create_security_group_rule(self, *args, **kwargs):
        """
        Create a specific rule from a specific security group.
        :rtype: dict
        """
        raise RewriteException()

    def delete_security_group_rule(self, security_group_rule_id, *args, **kwargs):
        """
        Delete a specific rule info from a specific security group.
        :param security_group_rule_id: security group rule id.
        :rtype: dict
        """
        raise RewriteException()

    def list_vpcs(self, *args, **kwargs):
        """
        Get network list.
        :rtype: dict
        """
        raise RewriteException()

    def create_vpc(self, *args, **kwargs):
        """
        Create a network.
        :rtype: dict
        """
        raise RewriteException()

    def delete_vpc(self, vpc_id, *args, **kwargs):
        """
        Delete a specific network.
        :param vpc_id: vpc id
        :rtype: dict
        """
        raise RewriteException()

    def modify_vpc(self, vpc_id, *args, **kwargs):
        """
        Modify a specific network.
        :param vpc_id: vpc id.
        :rtype: dict
        """
        raise RewriteException()

    def list_eips(self, *args, **kwargs):
        """
        Get a public ip address from a specific vm.
        :rtype: dict
        """
        raise RewriteException()

    def list_subnets(self, *args, **kwargs):
        """
        Get subnet list.
        :rtype: dict
        """
        raise RewriteException()

    def create_subnet(self, *args, **kwargs):
        """
        Create a subnet from a specific network.
        :rtype: dict
        """
        raise RewriteException()

    def delete_subnet(self, subnet_id, *args, **kwargs):
        """
        Delete a specific subnet from a specific network.
        :param subnet_id: subnet id.
        :rtype: dict
        """
        raise RewriteException()

    def modify_subnet(self, subnet_id, *args, **kwargs):
        """
        Modify a specific subnet from a specific network.
        :param subnet_id: subnet id.
        :rtype: dict
        """
        raise RewriteException()

    # ------------------***** charge *****-------------------
    def get_virtual_cost(self, *args, **kwargs):
        """
        Get current cost budget.
        :rtype: dict
        """
        raise RewriteException()

    # ------------------***** monitor *****-------------------
    def get_monitor_data(self, *args, **kwargs):
        """
        Get monitor data from a specific vm.
        :rtype: dict
        """
        raise RewriteException()


class PublicCloudManage(CloudManageBase):
    """Public Cloud Manage class.

    The object defines multiple proper methods for public cloud.
    """

    def get_spec_price(self, *args, **kwargs):
        """
        Get specific vm price.
        :rtype: dict
        """
        raise RewriteException()

    def list_instance_type_families(self, *args, **kwargs):
        """
        Get instance type families.
        :rtype: dict
        """
        raise RewriteException()

    def renew_vm(self, vm_id, *args, **kwargs):
        """
        Renew a specific vm.
        :param vm_id: vm id.
        :rtype: dict
        """
        raise RewriteException()

    # ------------------***** storage *****-------------------
    def list_buckets(self, *args, **kwargs):
        """
        Get block storage list.
        :rtype: dict
        """
        raise RewriteException()

    # ------------------***** charge *****-------------------
    def get_real_cost(self, *args, **kwargs):
        """
        Get real cost.
        :rtype: dict
        """
        raise RewriteException()


class PrivateCloudManage(CloudManageBase):
    """Private Cloud Manage class.

    The object defines multiple proper methods for private cloud.
    """

    # ------------------***** compute *****-------------------
    def list_hosts(self, *args, **kwargs):
        """
        Get host list.
        :rtype: dict
        """
        raise RewriteException()

    def list_clusters(self, *args, **kwargs):
        """
        Get cluster list.
        :rtype: dict
        """
        raise RewriteException()

    # ------------------***** storage *****-------------------
    def list_local_storage(self, *args, **kwargs):
        """
        Get local storage list.
        :rtype: dict
        """
        raise RewriteException()
