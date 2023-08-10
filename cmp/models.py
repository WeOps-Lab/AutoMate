# 统一管理CMP的 Model


class Model:
    pass


class VM(Model):
    RUNNING = "RUNNING"
    STOP = "STOP"
    ERROR = "ERROR"
    BUILD = "BUILD"
    PENDING = "PENDING"

    IN_USE = "IN_USE"
    EXPIRED = "EXPIRED"
    PROTECTIVELY_ISOLATED = "PROTECTIVELY_ISOLATED"

    PREPAID = "PREPAID"
    POSTPAID_BY_HOUR = "POSTPAID_BY_HOUR"
    UNKNOWN = "UNKNOWN"

    VM_STATUS_CHOICES = ((RUNNING, "运行中"), (STOP, "已关机"), (ERROR, "错误"), (BUILD, "创建中"), (PENDING, "配置中"))

    RESTRICT_STATE_CHOICES = ((IN_USE, "正常"), (EXPIRED, "过期"), (PROTECTIVELY_ISOLATED, "安全隔离"))

    CHARGE_TYPE_CHOICES = ((PREPAID, "包年包月"), (POSTPAID_BY_HOUR, "按量计费"), (UNKNOWN, "未知计费类型"))


class Disk(Model):
    UNATTACHED = "UNATTACHED"
    ATTACHED = "ATTACHED"
    ERROR = "ERROR"
    PENDING = "PENDING"

    SYSTEM_DISK = "SYSTEM_DISK"
    DATA_DISK = "DATA_DISK"

    CLOUD_BASIC = "CLOUD_BASIC"
    CLOUD_EFFICIENCY = "CLOUD_EFFICIENCY"
    CLOUD_SSD = "CLOUD_SSD"
    CLOUD_ESSD = "CLOUD_ESSD"
    CLOUD_UNKNOWN = "CLOUD_UNKNOWN"

    PREPAID = "PREPAID"
    POSTPAID_BY_HOUR = "POSTPAID_BY_HOUR"
    UNKNOWN = "UNKNOWN"

    DISK_STATUS_CHOICES = ((UNATTACHED, "未挂载"), (ATTACHED, "已挂载"), (ERROR, "错误"), (PENDING, "配置中"))

    DISK_TYPE_CHOICES = ((SYSTEM_DISK, "系统盘"), (DATA_DISK, "数据盘"))

    DISK_CATEGORY_CHOICES = (
        (CLOUD_BASIC, "普通云盘"),
        (CLOUD_EFFICIENCY, "高效云盘"),
        (CLOUD_SSD, "SSD云盘"),
        (CLOUD_ESSD, "ESSD云盘"),
        (CLOUD_UNKNOWN, "未知云盘"),
    )

    CHARGE_TYPE_CHOICES = ((PREPAID, "包年包月"), (POSTPAID_BY_HOUR, "按量计费"), (UNKNOWN, "未知计费类型"))


class Snapshot(Model):
    # 避免和长度常量 NORMAL 冲突
    AVAILABLE = "NORMAL"
    CREATING = "CREATING"
    ROLLBACKING = "ROLLBACKING"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"

    DISK_SNAPSHOT = "DISK_SNAPSHOT"
    VM_SNAPSHOT = "VM_SNAPSHOT"

    STATUS_CHOICES = ((AVAILABLE, "正常"), (CREATING, "创建中"), (ROLLBACKING, "回滚中"), (ERROR, "错误"), (UNKNOWN, "未知"))
    SNAPSHOT_TYPE_CHOICES = ((DISK_SNAPSHOT, "磁盘快照"), (VM_SNAPSHOT, "虚拟机快照"))


class Image(Model):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    OTHERS = "OTHERS"
    MARKETPLACE = "MARKETPLACE"

    WINDOWS = "WINDOWS"
    LINUX = "LINUX"
    UNKNOWN = "UNKNOWN"

    UNAVAILABLE = "UNAVAILABLE"
    AVAILABLE = "AVAILABLE"
    CREATING = "CREATING"
    ERROR = "ERROR"

    IMAGE_TYPE_CHOICES = ((PUBLIC, "公共镜像"), (PRIVATE, "私有镜像"), (OTHERS, "其他"), (MARKETPLACE, "镜像市场镜像"))

    OS_TYPE_CHOICES = ((WINDOWS, "WINDOWS"), (LINUX, "LINUX"), (UNKNOWN, "未知"))

    STATUS_CHOICES = ((UNAVAILABLE, "不可用"), (AVAILABLE, "可用"), (CREATING, "创建中"), (ERROR, "创建失败"))


class VPC(Model):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    ERROR = "ERROR"

    STATUS_CHOICES = ((PENDING, "配置中"), (AVAILABLE, "可用"), (ERROR, "错误"))


class Subnet(Model):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    ERROR = "ERROR"

    STATUS_CHOICES = ((PENDING, "配置中"), (AVAILABLE, "可用"), (ERROR, "错误"))


class SecurityGroup(Model):
    pass


class Eip(Model):
    CREATING = "CREATING"
    BINDING = "BINDING"
    BIND = "BIND"
    UNBINDING = "UNBINDING"
    UNBIND = "UNBIND"
    UNKNOWN = "UNKNOWN"

    PREPAID = "PREPAID"
    POSTPAID_BY_HOUR = "POSTPAID_BY_HOUR"
    UNKNOWN_PAID = "UNKNOWN_PAID"

    STATUS_CHOICES = (
        (CREATING, "创建中"),
        (BINDING, "绑定中"),
        (BIND, "已绑定"),
        (UNBINDING, "解绑中"),
        (UNBIND, "未绑定"),
        (UNKNOWN, "未知"),
    )

    CHARGE_TYPE_CHOICES = (
        (PREPAID, "包年包月"),
        (POSTPAID_BY_HOUR, "按量计费"),
        (UNKNOWN_PAID, "未知计费类型"),
    )


class PrivateStorage(Model):
    AVAILABLE = "AVAILABLE"
    PENDING = "PENDING"
    ERROR = "ERROR"

    STATUS_CHOICES = ((AVAILABLE, "可用"), (PENDING, "配置中"), (ERROR, "异常"))


class HostMachine(Model):
    pass


class Cluster(Model):
    AVAILABLE = "AVAILABLE"
    PENDING = "PENDING"
    ERROR = "ERROR"

    STATUS_CHOICES = ((AVAILABLE, "可用"), (PENDING, "配置中"), (ERROR, "异常"))


class Bucket(Model):
    STANDARD = "STANDARD"
    IA = "IA"
    ARCHIVE = "ARCHIVE"
    UNKNOWN = "unknown"

    BUCKET_TYPE_TYPE = (
        (STANDARD, "标准存储"),
        (IA, "低频存储"),
        (ARCHIVE, "归档存储"),
        (UNKNOWN, "未知存储"),
    )


class Redis(Model):
    TO_BE_INIT = 0
    PROCESSING = 1
    RUNNING = 2
    ISOLATION = -2
    TO_BE_DELETE = -3

    STATUS_CHOICES = (
        (TO_BE_INIT, "待初始化"),
        (PROCESSING, "流程中"),
        (RUNNING, "运行中"),
        (ISOLATION, "已隔离"),
        (TO_BE_DELETE, "待删除"),
    )

    INS_CLUSTER28 = 1
    INS_MASTER_SLAVER28 = 2
    INS_MASTER_SLAVER32 = 3
    INS_CLUSTER32 = 4
    INS_STAND_ALONE28 = 5
    INS_MASTER_SLAVER40 = 6
    INS_CLUSTER40 = 7
    REDIS_MASTER_SLAVE50 = 8
    REDIS_CLUSTER50 = 9

    INS_TYPE_CHOICES = (
        (INS_CLUSTER28, "Redis2.8集群版"),
        (INS_MASTER_SLAVER28, "Redis2.8主从版"),
        (INS_MASTER_SLAVER32, "Redis3.2主从版"),
        (INS_CLUSTER32, "Redis3.2集群版"),
        (INS_STAND_ALONE28, "Redis2.8单机版"),
        (INS_MASTER_SLAVER40, "Redis4.0主从版"),
        (INS_CLUSTER40, "Redis4.0集群版"),
        (REDIS_MASTER_SLAVE50, "Redis5.0主从版"),
        (REDIS_CLUSTER50, "Redis5.0集群版"),
    )

    CLUSTER = "cluster"
    MASTER_SLAVER = "masterslaver"
    STAND_ALONE = "standalone"
    CLUSTER28 = "cluster28"
    MASTER_SLAVER28 = "master_slaver28"
    MASTER_SLAVER32 = "master_slaver32"
    CLUSTER32 = "cluster32"
    STAND_ALONE28 = "stand_alone28"
    CLUSTER40 = "cluster40"

    TYPE_CHOICES = (
        (CLUSTER, "集群版"),
        (MASTER_SLAVER, "主从版"),
        (STAND_ALONE, "单机版"),
        (CLUSTER28, "Redis2.8集群版"),
        (MASTER_SLAVER28, "Redis2.8主从版"),
        (MASTER_SLAVER32, "Redis3.2主从版"),
        (CLUSTER32, "Redis3.2集群版"),
        (STAND_ALONE28, "Redis2.8单机版"),
        (CLUSTER40, "Redis4.0集群版"),
    )

    REDIS = "Redis"
    TCECKV = "TceCKV"

    ENGINE_CHOICES = ((REDIS, "社区版Redis"), (TCECKV, "TceCKV"))


class TDSQL(Model):
    NONACTIVATED = 0
    ACTIVATED = 1
    SHUTDOWN = 2
    OPENING = 3

    NOSHARD = "NOSHARD"
    GROUP = "GROUP"
    WAN_STATUS_CHOICES = ((NONACTIVATED, "未开通"), (ACTIVATED, "已开通"), (SHUTDOWN, "关闭"), (OPENING, "开通中"))
    INSTANCE_TYPE_CHOICES = ((NOSHARD, "非分布式"), (GROUP, "分布式"))

    # 状态目前没有文档，暂时用mariadb的
    CREATING = 0
    PROCESSING = 1
    RUNNING = 2
    UNINITIALIZED = 3
    INITIALIZING = 4
    QUARANTINED = -1
    DELETED = -2
    FAIL = -3
    UNKNOWN = -4
    STATUS_CHOICES = (
        (CREATING, "创建中"),
        (PROCESSING, "流程处理中"),
        (RUNNING, "运行中"),
        (UNINITIALIZED, "未初始化"),
        (INITIALIZING, "初始化中"),
        (QUARANTINED, "已隔离"),
        (DELETED, "已删除"),
        (FAIL, "创建超时"),
        (UNKNOWN, "未知"),
    )


class FileSystem(Model):
    AVAILABLE = "AVAILABLE"
    PENDING = "PENDING"
    ERROR = "ERROR"

    STATUS_CHOICES = ((AVAILABLE, "可用"), (PENDING, "配置中"), (ERROR, "异常"))


class PrivateBucket(Model):
    pass


class TKE(Model):
    MANAGED_CLUSTER = "MANAGED_CLUSTER"
    INDEPENDENT_CLUSTER = "INDEPENDENT_CLUSTER"
    TYPE_CHOICES = ((MANAGED_CLUSTER, "托管集群"), (INDEPENDENT_CLUSTER, "独立集群"))

    CENTOS = "centos7.2x86_64"
    UBUNTU = "ubuntu16.04.1 LTSx86_64"
    OS_TYPE_CHOICES = ((CENTOS, "centos7.2x86_64"), (UBUNTU, "ubuntu16.04.1 LTSx86_64"))

    RUNNING = "Running"
    CREATING = "Creating"
    ABNORMAL = "Abnormal"
    INITIALIZING = "Initializing"
    STATUS_CHOICES = ((RUNNING, "运行中"), (CREATING, "创建中"), (ABNORMAL, "异常"), (INITIALIZING, "初始化"))


class Mongodb(Model):
    NONACTIVATED = 0
    ACTIVATED = 1
    SHUTDOWN = 2
    OPENING = 3
    WAN_STATUS_CHOICES = ((NONACTIVATED, "未开通"), (ACTIVATED, "已开通"), (SHUTDOWN, "关闭"), (OPENING, "开通中"))
    UNINITIALIZED = 0
    PROCESSING = 1
    RUNNING = 2
    DELETED = -2
    STATUS_CHOICES = (
        (UNINITIALIZED, "待初始化"),
        (PROCESSING, "流程执行中"),
        (RUNNING, "运行中"),
        (DELETED, "实例已过期"),
    )
    ClUSTERTYPE_CHOICES = (
        (0, "副本集实例"),
        (1, "分片实例"),
    )


class Application(Model):
    pass


class Mariadb(Model):
    NONACTIVATED = 0
    ACTIVATED = 1
    SHUTDOWN = 2
    OPENING = 3
    WAN_STATUS_CHOICES = ((NONACTIVATED, "未开通"), (ACTIVATED, "已开通"), (SHUTDOWN, "关闭"), (OPENING, "开通中"))

    CREATING = 0
    PROCESSING = 1
    RUNNING = 2
    UNINITIALIZED = 3
    QUARANTINED = -1
    DELETED = -2
    STATUS_CHOICES = (
        (CREATING, "创建中"),
        (PROCESSING, "流程处理中"),
        (RUNNING, "运行中"),
        (UNINITIALIZED, "未初始化"),
        (QUARANTINED, "已隔离"),
        (DELETED, "已删除"),
    )


class LoadBalancer(Model):
    OPEN = "OPEN"
    INTERNAL = "INTERNAL"

    NET_TYPE_CHOICES = (
        (OPEN, "公网属性"),
        (INTERNAL, "内网属性"),
    )

    IPV4 = "IPV4"
    IPV6 = "IPV6"

    IP_VERSION_CHOICES = ((IPV4, "IPV4"), (IPV6, "IPV6"))


class RegionInfo(Model):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"

    STATUS_CHOICES = ((AVAILABLE, "可用"), (UNAVAILABLE, "不可用"))


class SecurityGroupRule(Model):
    INGRESS = "INGRESS"
    EGRESS = "EGRESS"
    ALL = "ALL"

    DIRECTION_CHOICES = ((INGRESS, "安全组入方向"), (EGRESS, "安全组出方向"), (ALL, "不区分方向"))


class ZoneInfo(Model):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"

    STATUS_CHOICES = ((AVAILABLE, "可用"), (UNAVAILABLE, "不可用"))


class Tag(Model):
    BUILD_IN = "BUILD_IN"
    SELF_DEFINE = "SELF_DEFINE"

    TAG_TYPE_CHOICE = ((BUILD_IN, "内置标签"), (SELF_DEFINE, "自定义标签"))


class AccountConfig(Model):
    pass


class BucketFile(Model):
    pass


class Domain(Model):
    pass


class InstanceFamily(Model):
    pass


class InstanceType(Model):
    pass


class LoadBalancerListener(Model):
    pass


class ProjectInfo(Model):
    pass


class RelayRule(Model):
    pass


class ResourceInfos(Model):
    pass


class RouteEntry(Model):
    pass


class RouteTable(Model):
    pass


class ServerCertificate(Model):
    pass


class ServerGroup(Model):
    pass


class SnapshotPolicy(Model):
    pass


class TKECloudCluster(Model):
    pass


class TKECloudNodeList(Model):
    pass


class BMS(Model):
    pass


class CKafka(Model):
    pass


class TKEInstance(Model):
    pass
