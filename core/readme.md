# 核心模块层(Cores)

## 数据库层(DB)

> 内置集成sqlalchemy和redis的client

## 通用驱动层(Driver)

### 当前支持的驱动能力

- Ansible
  > Ansible Driver包含ADHoc和Playbook2种模式;
  >
  > 同时支持同步和异步调用方式.支持设置超时时间;
  >
  > 支持配置相关钩子即相应的HANDLE层,其中HANDLE包含以下几种模式
  > - event_handler
  > - status_handler
  > - artifacts_handler
  > - cancel_callback
  > - finished_callback

- JVM
  > 可调用JAR包中对应方法
- NetMiko
  > 针对网络设备进行ssh连接同时执行相关命令

>

- PURESNMP
  > 可通过SNMP协议连接操作网络设备
- RESTAPI
  > 可通过该驱动调用API
- COMMAND
  > 执行系统命令
- TERRAFORM
  > 针对云资源的自动化的计划设计,执行,销毁操作

## 通用异常层(Exception)

> 提供通用的异常基类,可继承或者自定义业务异常类
>
> 提供异常捕获的钩子返回对应的响应

## 通用表单层(Form)

> 提供常用的请求or响应的Response格式

## 日志层(Log)

> 提供日志详细的配置以及日志对象,其他地方需使用日志可引入该logger

## 消息队列(MQ)

> 提供Kafka的生产者和消费者的能力

## 通用服务层(Service)

> 提供抽象Service层以及子级的Ansible的Service层

示例

```python
class AnsibleAdHocService(DriverService):
    __driver_tag__ = "ansible"
    driver_run_fn = "run_local_adhoc"
    input_model = ADHocModel
    output_model = AdHocResult


```

### Service支持Hook能力

当前Hook支持

- pre_run(核心业务调用前)
- post_run(核心业务调用后)

示例

```python
from core.service.base import DriverService, pre_run, post_run


class MyService(DriverService):
    @pre_run
    def add_params(self):
        """_run前执行该语句"""
        pass

    @post_run
    def parser_resp(self):
        """_run后执行该语句"""
        pass
```

## 工具包(Utils)

> 提供与业务无关的一些通用能力

- 自动加载模块 -嵌套数据打平
- 字符处理
- 加解密
- 性能装饰器
- 模板加载器
- 全局线程池
- 凭据操作

## celery

> celeryconfig提供celery的配置

```python
from kombu.serialization import registry

from core.settings import settings

BROKER_URL = settings.celery_broker
CELERY_RESULT_BACKEND = settings.celery_backend

CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json", "application/text"]
registry.enable("json")
registry.enable("application/text")
CELERY_RESULT_EXPIRES = settings.celery_result_expires

CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_ENABLE_UTC = True

CELERY_TRACK_STARTED = True  # 记录任务正在运行running,而不是pending ,防止进程被kill掉,无法确认任务是否开始执行.
CELERY_MAX_TASKS_PER_CHILD = 100  # 一个worker处理最大任务数,防止内存泄露

```

## 通用数据格式化层(Format)

> 提供对Input/Output输出的格式化
> 提供了Input的凭据,采集输出格式转换基类

示例

```python
from core.format import CredentialFormat, format_util


class MysqlCredentialFormat(CredentialFormat):
    code = "ansible_credential_mysql"
    type = "ansible_credential"
    tag = "ansible.credential.mysql"
    name = "数据库凭据转换(ansible)"
    desc = "数据库凭据转换(ansible)"
    format_map = {"login_port": "port", "login_user": "user", "login_password": "password"}


# 
secret = {"port": 3306, "user": "user", "password": "password"} 
context = {} # 可加入全局变量来构建
credential = format_util.format_ansible_credential("mysql", secret, context)
```

## 引导程序(BootStrap,Init)
> 构建服务,构建路由,初始化操作等

## 配置文件(Settings)
> 项目配置,可在项目中对应环境文件如.env进行配置

## 任务管理器(Tasks)
> 提供任务的执行,查询,终止等操作,也可以配置相关Callback进行回调
