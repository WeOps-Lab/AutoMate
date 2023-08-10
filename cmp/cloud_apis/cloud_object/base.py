# -*- coding: utf-8 -*-


class BaseResourceInfo:
    """
    资源基础类
    """

    def __init__(self, cloud_type="", resource_id="", resource_name="", desc="", tag=[], extra={}):
        self.cloud_type = cloud_type
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.desc = desc
        self.tag = tag or []
        self.extra = extra or {}

    def to_dict(self):
        return self.__dict__


class TKECloudNodeList(BaseResourceInfo):
    """
    节点列表 class for TKE Platforms.
    """

    def __init__(
        self,
        name="",
        generate_name="mc_",
        self_link="",
        uuid="",
        creation_timestamp="",
        finalizers=[],
        cluster_name="",
        type="",
        ip="",
        port="",
        username="",
        phase="",
        **kwargs,
    ):
        """
        Initialize node object.
        """
        super(TKECloudNodeList, self).__init__(**kwargs)
        self.name = name
        self.generate_name = generate_name
        self.self_link = self_link
        self.uuid = uuid
        self.creation_timestamp = creation_timestamp
        self.finalizers = finalizers
        self.cluster_name = cluster_name
        self.type = type
        self.ip = ip
        self.port = port
        self.username = username
        self.phase = phase


class TKECloudClusters(BaseResourceInfo):
    """
    集群列表 class for TKE Platforms.
    """

    def __init__(
        self,
        name="",
        self_link="",
        uuid="",
        creation_timestamp="",
        labels={},
        finalizers=[],
        tenant_id="",
        display_name="",
        type="",
        version="",
        network_device="",
        clusterCIDR="",
        serviceCIDR="",
        dns_domain="",
        public_alternative_names=[],
        features={},
        properties={},
        machines={},
        kubelet_extra_args={},
        cluster_credential_ref={},
        etcd={},
        **kwargs,
    ):
        """
        Initialize node object.
        """
        super(TKECloudClusters, self).__init__(**kwargs)
        self.name = name
        self.self_link = self_link
        self.uuid = uuid
        self.creation_timestamp = creation_timestamp
        self.labels = labels
        self.finalizers = finalizers
        self.tenant_id = tenant_id
        self.display_name = display_name
        self.type = type
        self.version = version
        self.network_device = network_device
        self.clusterCIDR = clusterCIDR
        self.serviceCIDR = serviceCIDR
        self.dns_domain = dns_domain
        self.public_alternative_names = public_alternative_names
        self.features = features
        self.properties = properties
        self.machines = machines
        self.kubelet_extra_args = kubelet_extra_args
        self.cluster_credential_ref = cluster_credential_ref
        self.etcd = etcd


class Region(BaseResourceInfo):
    """
    Region class for Cloud Platforms.
    """

    def __init__(self, status="", **kwargs):
        """
        Initialize Region object.
        """
        super(Region, self).__init__(**kwargs)
        self.status = status


class Zone(BaseResourceInfo):
    """
    Zone class for Cloud Platforms.
    """

    def __init__(self, status="", region="", tce_zone_id=0, **kwargs):
        """
        Initialize Zone object.
        """
        super(Zone, self).__init__(**kwargs)
        self.status = status
        self.region = region
        self.tce_zone_id = tce_zone_id


class Project(BaseResourceInfo):
    """
    Project class for Cloud Platforms.
    """

    def __init__(self, enabled=True, **kwargs):
        """
        Initialize Project object..
        """
        super(Project, self).__init__(**kwargs)
        self.enabled = enabled


class Domain(BaseResourceInfo):
    """
    Domain class for Cloud Platforms
    """

    def __init__(self, enabled=True, **kwargs):
        """
        Initialize Domain object..
        """
        super(Domain, self).__init__(**kwargs)
        self.enabled = enabled


class InstanceTypeFamily(BaseResourceInfo):
    """
    实例规格族
    """

    def __init__(self, **kwargs):
        super(InstanceTypeFamily, self).__init__(**kwargs)


class InstanceType(BaseResourceInfo):
    """
    Flavor class for Cloud Platforms
    """

    def __init__(self, vcpus=0, memory=0, disk=0, instance_family="", project="", region="", zone="", **kwargs):
        """
        Initialize Flavor object..
        """
        super(InstanceType, self).__init__(**kwargs)
        self.vcpus = vcpus
        self.memory = memory
        self.disk = disk
        self.instance_family = instance_family
        self.project = project
        self.region = region
        self.zone = zone


class VM(BaseResourceInfo):
    """
    实例基本属性
    """

    def __init__(
        self,
        instance_type="",
        uuid="",
        vcpus=0,
        memory=0,
        image="",
        os_name="",
        restrict_state="IN_USE",
        status="RUNNING",
        inner_ip=[],
        public_ip=[],
        system_disk={},
        data_disk=[],
        charge_type="",
        internet_accessible={},
        vpc="",
        subnet="",
        security_group=[],
        project="",
        zone="",
        region="",
        login_settings={},
        create_time="",
        expired_time="",
        peak_period=None,
        host_id=None,
        **kwargs,
    ):
        """

        Args:
            **kwargs ():
        """
        super(VM, self).__init__(**kwargs)
        self.instance_type = instance_type
        self.uuid = uuid
        self.vcpus = vcpus
        self.memory = memory
        self.image = image or ""
        self.os_name = os_name or ""
        self.restrict_state = restrict_state
        self.status = status
        self.inner_ip = inner_ip
        self.public_ip = public_ip
        self.system_disk = system_disk
        self.data_disk = data_disk
        self.charge_type = charge_type
        self.internet_accessible = internet_accessible or {}
        self.vpc = vpc or ""
        self.subnet = subnet or ""
        self.security_group = security_group or ""
        self.project = project
        self.zone = zone
        self.region = region
        self.login_settings = login_settings
        self.create_time = create_time
        self.expired_time = expired_time
        self.peak_period = peak_period
        self.host_id = host_id


class Disk(BaseResourceInfo):
    """
    Disk class for Cloud Platforms
    """

    def __init__(
        self,
        disk_type="",
        disk_size=0,
        charge_type="",
        portable=True,
        snapshot_ability=True,
        status="",
        category="",
        is_attached=False,
        server_id="",
        create_time="",
        expired_time="",
        encrypt=True,
        delete_with_instance=True,
        serial_number="",
        storage="",
        project="",
        zone="",
        region="",
        snapshot_policy="",
        **kwargs,
    ):
        """
        Initialize Disk object..
        """
        super(Disk, self).__init__(**kwargs)
        self.disk_type = disk_type
        self.disk_size = disk_size
        self.charge_type = charge_type
        self.portable = portable
        self.snapshot_ability = snapshot_ability
        self.status = status
        self.category = category
        self.is_attached = is_attached
        self.server_id = server_id
        self.create_time = create_time
        self.expired_time = expired_time
        self.encrypt = encrypt
        self.delete_with_instance = delete_with_instance
        self.serial_number = serial_number
        self.storage = storage
        self.project = project
        self.zone = zone
        self.region = region
        self.snapshot_policy = snapshot_policy


class Snapshot(BaseResourceInfo):
    """
    Snapshot class for Cloud Platforms
    """

    def __init__(
        self,
        disk_type="",
        disk_id="",
        disk_size=0,
        snapshot_type="DISK_SNAPSHOT",
        status="",
        create_time="",
        expired_time="",
        encrypt=True,
        is_permanent=True,
        server_id="",
        project="",
        zone="",
        region="",
        **kwargs,
    ):
        """
        Initialize Snapshot object..
        """
        super(Snapshot, self).__init__(**kwargs)
        self.disk_type = disk_type
        self.disk_id = disk_id
        self.disk_size = disk_size
        self.snapshot_type = snapshot_type
        self.status = status
        self.create_time = create_time
        self.expired_time = expired_time
        self.encrypt = encrypt
        self.is_permanent = is_permanent
        self.server_id = server_id
        self.project = project
        self.zone = zone
        self.region = region


class SnapshotPolicy(BaseResourceInfo):
    def __init__(
        self,
        time_points="",
        status="",
        retention_days=-1,
        repeat_week=[],
        disk_nums=0,
        create_time="",
        region="",
        zone="",
        **kwargs,
    ):
        super(SnapshotPolicy, self).__init__(**kwargs)
        self.time_points = time_points
        self.status = status
        self.retention_days = retention_days
        self.repeat_week = repeat_week
        self.disk_nums = disk_nums
        self.create_time = create_time
        self.region = region
        self.zone = zone


class Image(BaseResourceInfo):
    """
    Image class for Cloud Platforms
    """

    def __init__(
        self,
        create_time="",
        image_family="",
        arch="",
        image_type="",
        image_version="",
        os_name="",
        os_name_en="",
        os_type="",
        size=0,
        status="",
        image_format="",
        platform="",
        project="",
        **kwargs,
    ):
        """
        Initialize Image object..
        """
        super(Image, self).__init__(**kwargs)
        self.create_time = create_time
        self.image_family = image_family
        self.arch = arch
        self.image_type = image_type
        self.image_version = image_version
        self.os_name = os_name
        self.os_name_en = os_name_en
        self.os_type = os_type
        self.size = size
        self.status = status
        self.image_format = image_format
        self.platform = platform
        self.project = project


class SecurityGroup(BaseResourceInfo):
    """
    SecurityGroup class for Cloud Platforms
    """

    def __init__(
        self, is_default=False, create_time="", resource_group="", vpc="", project="", zone="", region="", **kwargs
    ):
        """
        Initialize SecurityGroup object..
        """
        super(SecurityGroup, self).__init__(**kwargs)
        self.is_default = is_default
        self.create_time = create_time
        self.resource_group = resource_group
        self.vpc = vpc
        self.project = project
        self.zone = zone
        self.region = region


class SecurityGroupRule(BaseResourceInfo):
    """
    SecurityGroupRule class for Cloud Platforms
    """

    def __init__(
        self,
        direction="",
        dest_cidr="",
        dest_group_id="",
        source_cidr="",
        source_group_id="",
        create_time="",
        modify_time="",
        nic_type="",
        protocol="",
        port_range="",
        priority="",
        security_group="",
        action="",
        project="",
        zone="",
        region="",
        **kwargs,
    ):
        """
        Initialize SecurityGroupRule object..
        """
        super(SecurityGroupRule, self).__init__(**kwargs)
        self.direction = direction
        self.dest_cidr = dest_cidr
        self.dest_group_id = dest_group_id
        self.source_cidr = source_cidr
        self.source_group_id = source_group_id
        self.create_time = create_time
        self.modify_time = modify_time
        self.nic_type = nic_type
        self.protocol = protocol
        self.port_range = port_range
        self.priority = priority
        self.security_group = security_group
        self.action = action
        self.project = project
        self.zone = zone
        self.region = region


class VPC(BaseResourceInfo):
    """
    VPC class for Cloud Platforms
    """

    def __init__(
        self,
        status="",
        cidr="",
        cidr_v6="",
        router="",
        router_tables=[],
        resource_group="",
        is_default=False,
        create_time="",
        dns=[],
        host="",
        project="",
        zone="",
        region="",
        **kwargs,
    ):
        """
        Initialize VPC object..
        """
        super(VPC, self).__init__(**kwargs)
        self.status = status
        self.cidr = cidr
        self.cidr_v6 = cidr_v6
        self.router = router
        self.router_tables = router_tables
        self.resource_group = resource_group
        self.is_default = is_default
        self.create_time = create_time
        self.dns = dns
        self.host = host
        self.project = project
        self.zone = zone
        self.region = region


class Subnet(BaseResourceInfo):
    """
    Subnet class for Cloud Platforms
    """

    def __init__(
        self,
        status="",
        gateway="",
        cidr="",
        cidr_v6="",
        vpc="",
        create_time="",
        router_table_id="",
        is_default=False,
        resource_group="",
        project="",
        zone="",
        region="",
        dns="",
        mask="",
        **kwargs,
    ):
        """
        Initialize Subnet object..
        """
        super(Subnet, self).__init__(**kwargs)
        self.status = status
        self.gateway = gateway
        self.cidr = cidr
        self.cidr_v6 = cidr_v6
        self.vpc = vpc
        self.create_time = create_time
        self.router_table_id = router_table_id
        self.is_default = is_default
        self.resource_group = resource_group
        self.project = project
        self.zone = zone
        self.region = region
        self.dns = dns
        self.mask = mask


class Eip(BaseResourceInfo):
    def __init__(
        self,
        status="",
        ip_addr="",
        instance_id="",
        create_time="",
        nic_id="",
        private_ip_addr="",
        is_attached="",
        bandwidth="",
        charge_type="",
        expired_time="",
        provider="",
        resource_group="",
        project="",
        zone="",
        region="",
        **kwargs,
    ):
        super(Eip, self).__init__(**kwargs)
        self.status = status
        self.ip_addr = ip_addr
        self.instance_id = instance_id
        self.create_time = create_time
        self.nic_id = nic_id
        self.private_ip_addr = private_ip_addr
        self.is_attached = is_attached
        self.bandwidth = bandwidth
        self.charge_type = charge_type
        self.expired_time = expired_time
        self.provider = provider
        self.resource_group = resource_group
        self.project = project
        self.zone = zone
        self.region = region


class HostMachine(BaseResourceInfo):
    """
    Host class for Cloud Platforms
    """

    def __init__(
        self,
        status="",
        connect_status="",
        power_status="",
        # ip_addr=[],
        # allocate_vcpus="",
        # allocate_memory="",
        # allocate_storage="",
        ip_addr="",
        ip_bmc="",
        hypervisor_type="",
        biz_region_id="",
        cpu="",
        memory="",
        local_storage="",
        cpu_usage="",
        memory_usage="",
        local_storage_usage="",
        memory_free="",
        cpu_free="",
        local_storage_free="",
        running_instances="",
        total_instances="",
        cluster_id="",
        project="",
        zone="",
        region="",
        **kwargs,
    ):
        """
        Initialize Host object..
        """
        super(HostMachine, self).__init__(**kwargs)
        self.status = status
        self.connect_status = connect_status
        self.power_status = power_status
        self.ip_addr = ip_addr
        self.ip_bmc = ip_bmc
        self.hypervisor_type = hypervisor_type
        self.biz_region_id = biz_region_id
        # self.allocate_vcpus = allocate_vcpus
        # self.allocate_memory = allocate_memory
        # self.allocate_storage = allocate_storage
        self.cpu = cpu
        self.memory = memory
        self.local_storage = local_storage
        self.memory_usage = memory_usage
        self.cpu_usage = cpu_usage
        self.local_storage_usage = local_storage_usage
        self.memory_free = memory_free
        self.cpu_free = cpu_free
        self.local_storage_free = local_storage_free
        self.running_instances = running_instances
        self.total_instances = total_instances
        self.cluster_id = cluster_id
        self.project = project
        self.zone = zone
        self.region = region


class PrivateStorage(BaseResourceInfo):
    """
    PrivateStorage class for Private Cloud Platforms
    """

    def __init__(
        self, status="", capacity="", used_capacity="", allocated_capacity="", host_id="", host_name="", **kwargs
    ):
        """
        Initialize Host object..
        """
        super(PrivateStorage, self).__init__(**kwargs)
        self.status = status
        self.capacity = capacity
        self.used_capacity = used_capacity
        self.allocated_capacity = allocated_capacity
        self.host_id = host_id
        self.host_name = host_name


class Bucket(BaseResourceInfo):
    def __init__(self, bucket_type="", create_time="", modify_time="", region="", **kwargs):
        super(Bucket, self).__init__(**kwargs)
        self.bucket_type = bucket_type
        self.create_time = create_time
        self.modify_time = modify_time
        self.region = region


class BucketFile(BaseResourceInfo):
    def __init__(self, create_time="", modify_time="", size=0, file_type="", parent="", bucket="", **kwargs):
        super(BucketFile, self).__init__(**kwargs)
        self.create_time = create_time
        self.modify_time = modify_time
        self.size = size
        self.type = file_type
        self.parent = parent
        self.bucket = bucket


# *************************************** TCE
class TKE(BaseResourceInfo):
    """base class of K8S"""

    def __init__(
        self,
        cluster_type="",
        network_settings={},
        os="",
        node_num=0,
        project="",
        status="",
        cluster_property="",
        master_node_num=0,
        image="",
        os_customize_type="",
        container_runtime="",
        create_time="",
        version="",
        **kwargs,
    ):
        super(TKE, self).__init__(**kwargs)
        self.cluster_type = cluster_type
        self.network_settings = network_settings
        self.os = os
        self.node_num = node_num
        self.project = project
        self.status = status
        self.cluster_property = cluster_property
        self.master_node_num = master_node_num
        self.image = image
        self.os_customize_type = os_customize_type
        self.container_runtime = container_runtime
        self.create_time = create_time
        self.version = version


class TKEInstance(BaseResourceInfo):
    """base class of tke cluster instance"""

    def __init__(
        self,
        cluster="",
        role="",
        status="",
        create_time="",
        drain_status="",
        failed_reason="",
        data_disk=[],
        labels=[],
        target="",
        docker_graph_path="",
        user_script="",
        unschedulable=0,
        extra_args="",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.cluster = cluster
        self.target = target
        self.labels = labels
        self.create_time = create_time
        self.docker_graph_path = docker_graph_path
        self.extra_args = extra_args
        self.user_script = user_script
        self.drain_status = drain_status
        self.unschedulable = unschedulable
        self.status = status
        self.role = role
        self.data_disk = data_disk
        self.failed_reason = failed_reason


class FileSystem(BaseResourceInfo):
    """
    base class of FileSystem
    """

    def __init__(
        self,
        vpc="",
        protocol="",
        status="",
        used_capacity=0,
        max_size=0,
        capacity_limit=0,
        allocated_capacity=0,
        storage_type="",
        pgroup={},
        create_time="",
        encrypt=False,
        zone="",
        ip_addr="",
        key="",
        mount_info=[],
        **kwargs,
    ):
        super(FileSystem, self).__init__(**kwargs)
        self.vpc = vpc
        self.protocol = protocol
        self.status = status
        self.used_capacity = used_capacity
        self.max_size = max_size
        self.capacity_limit = capacity_limit
        self.allocated_capacity = allocated_capacity
        self.storage_type = storage_type
        self.pgroup = pgroup
        self.create_time = create_time
        self.encrypt = encrypt
        self.zone = zone
        self.ip_addr = ip_addr
        self.key = key
        self.mount_info = mount_info


class LoadBalancer(BaseResourceInfo):
    """base class of loadbalance"""

    def __init__(
        self,
        net_type="",
        lb_type=True,
        domain="",
        vips=[],
        status=True,
        create_time="",
        status_time=0,
        project=0,
        region="",
        vpc="",
        ip_version="",
        expire_time="",
        charge_type={},
        ipv6_addr="",
        backend_servers=[],
        port=[],
        **kwargs,
    ):
        super(LoadBalancer, self).__init__(**kwargs)
        self.net_type = net_type
        self.lb_type = lb_type
        self.domain = domain or ""
        self.vips = vips or []
        self.status = status or True
        self.create_time = create_time or ""
        self.status_time = status_time or ""
        self.region = region or ""
        self.project = project or 0
        self.vpc = vpc or ""
        self.ip_version = ip_version or "IPV4"
        self.expire_time = expire_time or ""
        self.charge_type = charge_type or ""
        self.ipv6_addr = ipv6_addr or ""
        self.backend_servers = backend_servers
        self.port = port


class LoadBalancerListener(BaseResourceInfo):
    def __init__(
        self,
        front_version="",
        front_port="",
        backend_version="",
        backend_port="",
        status="RUNNING",
        listen_config={},
        server_group="",
        create_time="",
        region="",
        zone="",
        load_balancer="",
        **kwargs,
    ):
        super(LoadBalancerListener, self).__init__(**kwargs)
        self.front_version = front_version
        self.front_port = front_port
        self.backend_version = backend_version
        self.backend_port = backend_port
        self.status = status
        self.listen_config = listen_config
        self.server_group = server_group
        self.create_time = create_time
        self.region = region
        self.zone = zone
        self.load_balancer = load_balancer


class RouteTable(BaseResourceInfo):
    """base class of RouteTable"""

    def __init__(
        self, status="", vpc="", vrouter="", subnets=[], is_system=False, create_time="", zone="", region="", **kwargs
    ):
        super(RouteTable, self).__init__(**kwargs)
        self.status = status
        self.vpc = vpc
        self.vrouter = vrouter
        self.subnets = subnets
        self.is_system = is_system
        self.create_time = create_time
        self.zone = zone
        self.region = region


class RouteEntry(BaseResourceInfo):
    """base class of RouteEntry"""

    def __init__(
        self,
        status="",
        route_table="",
        cidr_block="",
        next_hops="",
        is_system=False,
        create_time="",
        zone="",
        region="",
        **kwargs,
    ):
        super(RouteEntry, self).__init__(**kwargs)
        self.status = status
        self.route_table = route_table
        self.cidr_block = cidr_block
        self.next_hops = next_hops
        self.is_system = is_system
        self.create_time = create_time
        self.zone = zone
        self.region = region


class VServerGroup(BaseResourceInfo):
    def __init__(
        self, backend_servers=[], load_balancer="", listens=[], rules=[], create_time="", region="", zone="", **kwargs
    ):
        super(VServerGroup, self).__init__(**kwargs)
        self.backend_servers = backend_servers
        self.load_balancer = load_balancer
        self.listens = listens
        self.rules = rules
        self.create_time = create_time
        self.region = region
        self.zone = zone


class ServerCertificate(BaseResourceInfo):
    def __init__(self, finger_print="", upload_time="", expired_time="", create_time="", region="", zone="", **kwargs):
        super(ServerCertificate, self).__init__(**kwargs)
        self.finger_print = finger_print
        self.upload_time = upload_time
        self.expired_time = expired_time
        self.create_time = create_time
        self.region = region
        self.zone = zone


class RelayRule(BaseResourceInfo):
    def __init__(
        self,
        url="",
        domain="",
        server_group="",
        load_balancer="",
        create_time="",
        region="",
        zone="",
        port="",
        protocal="",
        **kwargs,
    ):
        super(RelayRule, self).__init__(**kwargs)
        self.url = url
        self.domain = domain
        self.server_group = server_group
        self.load_balancer = load_balancer
        self.create_time = create_time
        self.region = region
        self.zone = zone
        self.protocal = protocal
        self.port = port


class Redis(BaseResourceInfo):
    """base class of Redis"""

    def __init__(
        self,
        project=0,
        region=0,
        zone=0,
        vpc=0,
        subnet=0,
        status=2,
        vip="",
        port=-3,
        create_time="",
        size="",
        used_size="",
        instance_type="",
        billing_mode=False,
        auto_renew_flag=False,
        offline_time="",
        deadline_time="",
        engine="",
        product_type="",
        instance_node=[],
        shard_size=0,
        shard_num=0,
        replicas_num=0,
        close_time="",
        slave_read_weight=0,
        project_name="",
        **kwargs,
    ):
        super(Redis, self).__init__(**kwargs)
        self.project = project
        self.region = region
        self.zone = zone
        self.vpc = vpc
        self.subnet = subnet
        self.status = status
        self.vip = vip
        self.port = port
        self.create_time = create_time
        self.size = size
        self.used_size = used_size
        self.instance_type = instance_type
        self.billing_mode = billing_mode
        self.auto_renew_flag = auto_renew_flag
        self.offline_time = offline_time
        self.deadline_time = deadline_time
        self.engine = engine
        self.product_type = product_type
        self.instance_node = instance_node
        self.shard_size = shard_size
        self.shard_num = shard_num
        self.replicas_num = replicas_num
        self.close_time = close_time
        self.slave_read_weight = slave_read_weight
        self.project_name = project_name


class MongoDB(BaseResourceInfo):
    """base class of Redis"""

    def __init__(
        self,
        region=0,
        zone=0,
        vpc=0,
        subnet=0,
        status=2,
        inner_port="",
        create_time="",
        memory=0,
        node_count=0,
        qps=0,
        inner_ip="",
        charge_type="",
        storage="",
        wan_status=0,
        wan_ip="",
        machine="",
        mongo_version="",
        cluster_type=0,
        **kwargs,
    ):
        super(MongoDB, self).__init__(**kwargs)
        self.region = region
        self.zone = zone
        self.vpc = vpc
        self.subnet = subnet
        self.status = status
        self.inner_port = inner_port
        self.create_time = create_time
        self.memory = memory
        self.node_count = node_count
        self.qps = qps
        self.inner_ip = inner_ip
        self.charge_type = charge_type
        self.storage = storage
        self.wan_status = wan_status
        self.wan_ip = wan_ip
        self.machine = machine
        self.cluster_type = cluster_type
        self.mongo_version = mongo_version


class Mariadb(BaseResourceInfo):
    """mariadb base class"""

    def __init__(
        self,
        region="",
        zone="",
        machine="",
        create_time="",
        update_time="",
        memory=0,
        node_count=0,
        qps=0,
        inner_ip="",
        charge_type="",
        storage=0,
        vpc="",
        subnet="",
        inner_port=0,
        wan_domain="",
        wan_status=0,
        wan_ip="",
        status=2,
        **kwargs,
    ):
        super(Mariadb, self).__init__(**kwargs)
        self.region = region
        self.zone = zone
        self.machine = machine
        self.create_time = create_time
        self.update_time = update_time
        self.memory = memory
        self.node_count = node_count
        self.qps = qps
        self.inner_ip = inner_ip
        self.charge_type = charge_type
        self.storage = storage
        self.vpc = vpc
        self.subnet = subnet
        self.inner_port = inner_port
        self.wan_domain = wan_domain
        self.wan_status = wan_status
        self.wan_ip = wan_ip
        self.status = status


class TDSQL(BaseResourceInfo):
    """tdsql base class"""

    def __init__(
        self,
        region="",
        zone="",
        project="",
        vpc=0,
        subnet=0,
        status=0,
        inner_ip="",
        inner_port="",
        create_time="",
        auto_renew_flag=False,
        memory=0,
        storage=0,
        shard_count=0,
        period_end_time="",
        isolated_time_stamp="",
        shard_detail=[],
        node_count=0,
        excluster_id=0,
        wan_domain="",
        wan_ip="",
        wan_port=0,
        update_time="",
        engine="",
        version="",
        pay_mode="",
        wan_status=0,
        instance_type="",
        **kwargs,
    ):
        super(TDSQL, self).__init__(**kwargs)
        self.region = region
        self.zone = zone
        self.project = project
        self.vpc = vpc
        self.subnet = subnet
        self.status = status
        self.inner_ip = inner_ip
        self.inner_port = inner_port
        self.create_time = create_time
        self.auto_renew_flag = auto_renew_flag
        self.memory = memory
        self.storage = storage
        self.shard_count = shard_count
        self.period_end_time = period_end_time
        self.isolated_time_stamp = isolated_time_stamp
        self.shard_detail = shard_detail
        self.node_count = node_count
        self.excluster_id = excluster_id
        self.wan_domain = wan_domain
        self.wan_ip = wan_ip
        self.wan_port = wan_port
        self.update_time = update_time
        self.engine = engine
        self.version = version
        self.pay_mode = pay_mode
        self.wan_status = wan_status
        self.instance_type = instance_type


class BMS(BaseResourceInfo):
    # 裸金属服务器
    def __init__(
        self,
        uuid="",
        raid_type="",
        os_type="",
        os_version="",
        private_ip="[]",
        flavor="",
        create_time="",
        status="",
        app_id="",
        region="",
        zone="",
        vpc="",
        subnet="",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.uuid = uuid
        self.raid_type = raid_type
        self.os_type = os_type
        self.os_version = os_version
        self.private_ip = private_ip
        self.flavor = flavor
        self.create_time = create_time
        self.status = status
        self.app_id = app_id
        self.region = region
        self.zone = zone
        self.vpc = vpc
        self.subnet = subnet


class CKafka(BaseResourceInfo):
    def __init__(
        self,
        vip="",
        v_port="",
        ip="",
        status=1,
        bandwidth=0,
        disk_size=0,
        tce_zone_id=0,
        vpc="",
        subnet="",
        renew_flag=1,
        healthy=0,
        healthy_message="",
        create_time="",
        expire_time="",
        is_internal=True,
        topic_num=0,
        version="",
        tce_zone_ids="",
        cvm=0,
        region="",
        zone="",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.vip = vip
        self.v_port = v_port
        self.ip = ip
        self.status = status
        self.bandwidth = bandwidth
        self.disk_size = disk_size
        self.tce_zone_id = tce_zone_id
        self.vpc = vpc
        self.subnet = subnet
        self.renew_flag = renew_flag
        self.healthy = healthy
        self.healthy_message = healthy_message
        self.create_time = create_time
        self.expire_time = expire_time
        self.is_internal = is_internal
        self.topic_num = topic_num
        self.version = version
        self.tce_zone_ids = tce_zone_ids
        self.cvm = cvm
        self.region = region
        self.zone = zone


class PrivateBucket(BaseResourceInfo):
    """base class of PrivateBucket"""

    def __init__(self, region="", **kwargs):
        super(PrivateBucket, self).__init__(**kwargs)
        self.region = region


class Tag:
    def __init__(self, key="", value="", tag_type="", desc="", **kwargs):
        super(Tag, self).__init__(**kwargs)
        self.key = key
        self.value = value
        self.tag_type = tag_type
        self.desc = desc

    def to_dict(self):
        return {"key": self.key, "value": self.value, "tag_type": self.tag_type, "desc": self.desc}


class Balance:
    """
    账单余额类。该类只做数据模板，无需持久化
    """

    def __init__(
        self,
        amount,  # type: float
        currency="",  # type: str
        unit="",  # type: str
        extra=None,  # type: dict
    ):
        self.amount = amount
        self.currency = currency
        self.unit = unit
        self.extra = extra

    def to_dict(self):
        return {"amount": self.amount, "currency": self.currency, "unit": self.unit, "extra": self.extra}


class Transactions:
    """
    消费记录类。该类只做数据模板，无需持久化
    """

    def __init__(
        self,
        amount,  # type: float
        transaction_time,  # type: str
        currency="",  # type: str
        unit="",  # type: str
        extra=None,  # type: dict
    ):
        self.amount = amount
        self.transaction_time = transaction_time
        self.currency = currency
        self.unit = unit
        self.extra = extra

    def to_dict(self):
        return {
            "amount": self.amount,
            "transaction_time": self.transaction_time,
            "currency": self.currency,
            "unit": self.unit,
            "extra": self.extra,
        }


class LocalStorage(BaseResourceInfo):
    """
    Local storgae class for Cloud Platforms
    """

    def __init__(
        self,
        storage_type="",  # type :str
        capacity=None,  # type: int
        used_capacity="",  # type: str
        allocated_capacity="",  # type: str
        linked_host_id=None,  # type: list
        linked_host_name=None,  # type: list
        **kwargs,
    ):
        """
        Initialize LocalStorage object..
        """
        super(LocalStorage, self).__init__(**kwargs)
        self.storage_type = storage_type
        self.capacity = capacity
        self.used_capacity = used_capacity
        self.allocated_capacity = allocated_capacity
        self.linked_host_id = linked_host_id
        self.linked_host_name = linked_host_name


class ZoneInstanceConfig:
    def __init__(
        self,
        zone,  # type str
        status,  # type str
        type_name,  # type str
        instance_family,  # type str
        price,  # type dict
        cpu,  # type int
        memory,  # type int
        instance_type,  # type str
        instance_charge_type,  # type str
    ):
        self.zone = zone
        self.status = status
        self.type_name = type_name
        self.instance_family = instance_family
        self.price = price
        self.cpu = cpu
        self.memory = memory
        self.instance_type = instance_type
        self.instance__charge_type = instance_charge_type

    def to_dict(self):
        return {
            "zone": self.zone,
            "status": self.status,
            "type_name": self.type_name,
            "price": self.price,
            "instance_family": self.instance_family,
            "cpu": self.cpu,
            "memory": self.memory,
            "instance_type": self.instance_type,
            "instance_charge_type": self.instance__charge_type,
        }


class FusionCloudDiskType:
    def __init__(
        self,
        cloud_type,
        resource_id,
        resource_name="",
        desc="",
        is_public=False,
        qos_specs_id="",
        extra={},
        project="",
        region="",
    ):
        self.region = region
        self.project = project
        self.cloud_type = cloud_type
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.desc = desc
        self.is_public = is_public
        self.qos_specs_id = qos_specs_id
        self.extra = extra

    def to_dict(self):
        return {
            "cloud_type": self.cloud_type,
            "region": self.region,
            "project": self.project,
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
            "desc": self.desc,
            "is_public": self.is_public,
            "qos_specs_id": self.qos_specs_id,
            "extra": self.extra,
        }


class Cluster(BaseResourceInfo):
    """
    集群基本属性
    """

    def __init__(
        self,
        status="",
        ds_num=0,
        vm_num=0,
        net_num=0,
        ds_sum=0,
        ds_usage=0,
        ds_free=0,
        cpu_sum=0,
        cpu_usage=0,
        cpu_free=0,
        memory_sum=0,
        memory_usage=0,
        memory_free=0,
        **kwargs,
    ):
        """

        Args:
            **kwargs ():
        """
        super().__init__(**kwargs)
        self.status = status
        self.ds_num = ds_num
        self.vm_num = vm_num
        self.net_num = net_num
        self.ds_sum = ds_sum
        self.ds_usage = ds_usage
        self.ds_free = ds_free
        self.cpu_sum = cpu_sum
        self.cpu_usage = cpu_usage
        self.cpu_free = cpu_free
        self.memory_sum = memory_sum
        self.memory_usage = memory_usage
        self.memory_free = memory_free


class Application(BaseResourceInfo):
    def __init__(
        self,
        application_type="",
        microservice_type="",
        prog_lang="",
        application_runtime_type="",
        application_resource_type="",
        create_time="",
        update_time="",
        apigateway_service_id="",
        group_count=0,
        instance_count=0,
        runinstance_count=0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.application_type = application_type
        self.microservice_type = microservice_type
        self.prog_lang = prog_lang
        self.application_runtime_type = application_runtime_type
        self.application_resource_type = application_resource_type
        self.create_time = create_time
        self.update_time = update_time
        self.apigateway_service_id = apigateway_service_id
        self.group_count = group_count
        self.instance_count = instance_count
        self.runinstance_count = runinstance_count


# manageone
class DataStore(BaseResourceInfo):
    def __init__(self, ip_addr="", storage_gb="", biz_region_id="", **kwargs):
        super().__init__(**kwargs)
        self.ip_addr = ip_addr
        self.storage_gb = storage_gb
        self.biz_region_id = biz_region_id


class BusinessRegion(BaseResourceInfo):
    def __init__(self, cloud_version="", brand="", vcpus="", memory_mb="", storage_gb="", **kwargs):
        super().__init__(**kwargs)
        self.cloud_version = cloud_version
        self.brand = brand
        self.vcpus = vcpus
        self.memory_mb = memory_mb
        self.storage_gb = storage_gb
