
# 云平台插件开发

> 该文档用于开发Automate的云平台插件，提供扩展云平台的能力，包含对新的云平台及云资产的采集和监控能力，同时结合weops的云平台模板对其进行采集纳管，监控，视图管理等。采用新版监控链路推送，稳定可观测。其中涉及与CMDB模型和关联关系，监控指标等关联，请详细阅读以下内容。

## 目录结构

```markdown
cmp_plugins
├── README.md  # 帮助文档
├── requirements.txt
└── templatecloud          # 新的云平台目录
    ├── __init__.py
    ├── format             # 格式转换目录
    │   ├── __init__.py
    │   ├── collect.py      # 采集格式转换文件
    │   └── credential.py   # 凭据转换文件
    └── resource_apis
        ├── __init__.py
        └── cw_templatecloud.py  # 核心插件文件,命名无要求
```

如果需要新建一个云,可拷贝templatecloud目录,重命名为newcloud

## 开发规范

### Format

#### Collect 采集格式化

> 定义采集的字段,以及丰富字段能力.支持基础映射支持mako语法(更建议mako语法,功能更强大)

- 常用语法

```python
from core.driver.cmp.collect import CMPCollectFormat


class NewCloudFormat(CMPCollectFormat):
    code = "cmp_collect_newcloud"  # 格式`cmp_collect_{newcloud}` 前缀必须固定,后缀使用cmdb模型分类id,否则会影响采集能力
    type = "cmp_collect"  # 无需修改
    tag = "cmp.collect.fusion_insight"  # 暂无意义,用于标记此云,可按格式`"cmp.collect.{newcloud}`
    name = "XX云数据转换(cmp)"  # 中文名
    desc = "XX云数据转换(cmp)"  # 详细描述
    assoc_key = "resource_id"  # 关联key,即云对象的唯一值,用于多对象构建关联使用
    format_map = {}
```

> format_map支持单对象和多对象

- 单对象

```python
format_map = {
    "resource_name": "hostname",
    "resource_id": "hostname",
    "ip_addr": "ip",
    "vcpus": "cpuCores",
    "memory_mb": "totalMemory",
    "storage_gb": "totalHardDiskSpace",
    "status": "runningStatus",
    "os_name": "osType",
    "bk_inst_name": "${'%s-%s-%s'%(hostname,clusterName,account_name)}",  
}
```

tips:

1. bk_inst_name必传,用来定义cmdb的唯一名,格式可使用mako语法自定义 
2. cmdb实例属性如设计为字符串,需使用mako手动转化,如 `"${str(xx)}"` 否则纳管时会报类型错误
3. 可以使用context传入的key,如account_name

- 多对象

```python
assoc_key = "resource_id"  # 关联key,即云对象的唯一值,用于多对象构建关联使用
format_map = {
    "fusioninsight_cluster": {
        "bk_inst_name": "${'%s-%s-%s'%(name,id,account_name)}",
        "fusioninsight_account": "${account_name}",
        "resource_name": "name",
        "resource_id": "${str(id)}",
    },
    "fusioninsight_host": {
        "resource_name": "hostname",
        "resource_id": "hostname",
        "ip_addr": "ip",
        "vcpus": "cpuCores",
        "memory_mb": "totalMemory",
        "storage_gb": "totalHardDiskSpace",
        "status": "runningStatus",
        "os_name": "osType",
        "bk_inst_name": "${'%s-%s-%s'%(hostname,clusterName,account_name)}",
        "fusioninsight_cluster": "${fusioninsight_cluster_map[str(clusterId)]}"
    }
}
```

tips:
1. 每个key均为cmdb模型ID,写错无法进行纳管
2. assoc_key必须得有,value为其云资产的唯一值,用于寻找实例之间的关联
3. 关联关系的构建需要定义对应key,否则无法对构建其关联关系,即每个对象与另一个对象只能构建一个关联,多个暂不支持如
> `"fusioninsight_account": "${account_name}"`
> 
> 其值必须为关联关系对象的bk_inst_name
> `"fusioninsight_cluster": "${fusioninsight_cluster_map[str(clusterId)]}"`
4. 字典有顺序,即纳管CMDB资产逻辑顺序,务必从上至下进行编写

5. 内置{bk_obj_id}_map,构建所有资产列表的map,便于下面的对象进行关联构建;
   
    格式为
    ```
    {bk_obj_id}_map={assoc_key_value:bk_inst_name} 
    > assoc_key_value即assoc_key定义的value
    > bk_inst_name即关联的对象bk_obj_id的bk_inst_name
    ```
    用法可参考
    `"fusioninsight_cluster": "${fusioninsight_cluster_map[str(clusterId)]}"`


6. 可以使用context传入的key,如account_name



#### Credential格式化

> 用于构建凭据到Driver层的映射,便于从vault中获取凭据后转换进入Driver层
```python
from core.driver.cmp.credential import CMPCredentialFormat
class NewCloudFormat(CMPCredentialFormat):
    code = "cmp_credential_newcloud"  # 格式`cmp_credential_{newcloud}` 前缀必须固定,后缀使用cmdb模型分类,否则会影响凭据获取
    type = "cmp_credential"  # 无需修改
    tag = "cmp.credential.newcloud"  # 暂无意义,用于标记此云,可按格式`"cmp.credential.{newcloud}`
    name = "XX云数据凭据转换(cmp)"  # 中文名
    desc = "XX云数据凭据转换(cmp)"  # 详细描述
    format_map = {"account": "username", "password": "password"}
```


tips:
1. format_map的key是不能修改的,为Driver层的入参,value值分别对应vault管理中的账号和密码的key
```python
# 账号密码型
format_map = {"account": "username", "password": "password"}
# ak/sk型
format_map = {"account": "ak", "password": "sk"}
```

####  MakoFormat详细介绍

> 参考 [MakoFormat测试案例](../tests/core/format/mako_format_test.py)

tips:
1. 支持字典key映射,如`"resource_name": "resourceName"`
2. 支持字典嵌套映射,如`"resource_name": "resourceName.xx"`
3. 支持列表下标,如`"inner_ip": "resourceIp.0"`
4. 支持mako语法引用变量,即`${key}`,如`"bk_obj_id": "${vm_obj}"`
5. 支持沙箱,可支持的语法较多
    - 字符串拼接
    语法: `${"prefix" + K
      EY}`、`${"prefix%s" % KEY}`、`${"prefix{}".format(KEY)}`、`${"%s%s" % (KEY1, KEY2)}`

    - 字符串变换
      语法：`${KEY.upper()}`、`${KEY.replace("\n", ",")}`、`${KEY[0:2]}、${KEY.strip()}`
      
    - 数字运算
      语法：`${int(KEY) + 1}`、`${int(KEY)/10}`
      
    - 类型转换
      语法：`${KEY.split("\n")}`、`${KEY.count()}`、`${list(KEY)}`、`${[item.strip() for item in KEY.split("\n")]}`
      
    - 复杂类型取值
      语法：`${KEY["a"]["b"]}`,`${KEY[1][2]["a"]}`   
      
    - 支持的python内置函数
    ```text
        ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__import__', 'datetime', 're', 'hashlib', 'random', 'time', 'os']
    ```
    
6. 支持字段重写,入参item为此次迭代的字典,context为全局变量
    - 单对象单key重写`get_{key}`   
    - 多对象单key重写`get_{bk_obj_id}_{key}` 
    - 统一重写 `get`
    



### 云平台API

> 目录：cmp_plugins/xxcloud/resource_apis/cw_xxcloud

####  类设计

> 参考 [云API模板](templatecloud/resource_apis/cw_templatecloud.py)

包含2种类设计，如多个版本，可设计多个XXCloud

- CwXXCloud 》 云平台基础类，用于认证以及一些版本管理

  - CwXXCloud务必添加`@register`

  - ```python
    from cmp.cloud_apis.resource_client import register
    @register
    class CwTemplateCloud(object):
      pass
    ```


   - XXCloud 》用于对接某版本各种增删改查API接口类，如查询虚机，查询所有资源，查询监控数据

     - `list_vms` 虚拟机列表接口（单对象）

     - `list_hosts` 宿主机列表接口（单对象）

       - 返回格式	
     
        ```json
          {
            "result": true,
            "data": [
              {
                "resource_id": "123",
                "resource_name": "vm_test_1"
              },
              {
                "resource_id": "456",
                "resource_name": "vm_test_1"
              }
            ]
          }
        ```

     - `list_hosts` 宿主机列表接口（单对象）

     - `list_xxs`其他实例列表接口（单对象）
     
     - `list_all_resouces` 获取所有资源（多对象）
     
       - 返回格式
     
       ```json
        {
                "result": true,
                "data": {
                  "template_vms": [   # template_vms为某云虚拟机的bk_obj_id
                    {
                      "resource_id": "123",
                      "resource_name": "vm_test_1"
                    },
                    {
                      "resource_id": "456",
                      "resource_name": "vm_test_1"
                    }
                  ],
                  "template_ds": [    # template_ds为某云存储的bk_obj_id
                    {
                      "resource_id": "123",
                      "resource_name": "ds_test_1"
                    },
                    {
                      "resource_id": "456",
                      "resource_name": "ds_test_1"
                    }
                  ]
                }
              }
       ```
     
     - `get_weops_monitor_data`获取监控数据
     
       - 入参kwargs
     
       | 参数       | 描述                     | 是否必填 | 举例                       |
       | ---------- | ------------------------ | -------- | -------------------------- |
       | StartTime  | 起始时间                 | 否       | 2023-7-25 10:10:00         |
       | EndTime    | 结束时间                 | 否       | 2023-7-25 10:15:00         |
       | Period     | 时间间隔（s）            | 否       | 300                        |
       | resourceId | 资源实例id，多个逗号分割 | 是       | vm-01,vm-02                |
       | Metrics    | 指标名，列表             | 是       | ["cpuUsage","totalMemory"] |
       | context    | 上下文，用于识别多对象   | 是       | 看下面👇🏻                   |
     
         - context格式
     
       ```json
       {
         "resource"：[
           {
             "bk_obj_id": "qcloud_cvm",
             "bk_inst_id": 111,
             "resource_id": "ins-qnopai6m",
             "bk_inst_name": "深信服",
             "bk_biz_id": 2
           },
           {
             "bk_obj_id": "qcloud_cvm",
             "bk_inst_id": 222,
             "resource_id": "ins-0g4ehetc",
             "bk_inst_name": "autopack",
             "bk_biz_id": 2
           }
        ]
       }
       ```
     
       - 无维度返回格式
     
       ```json
       {'result': True, 'data': 
           {'MRS-MN-02': 
               {
                 'cpuUsage': [(1689585060000, 4.0)], 
                 'memoryUsedRatio': [(1689585060000, 0.11)]
               }, 
            'MRS-MN-01': 
                {'cpuUsage': [(1689585060000, 2.0)], 
                 'memoryUsedRatio': [(1689585060000, 0.04)]
                }
           }
       }
       ```
     
       - 有维度返回格式
     
       ```json
       {'result': True, 'data': 
           {'MRS-MN-02': 
               {'freeSpace': 
                   {
                     (('mountPoint', '/'),): [(1689585060000, 14.66)], 
                     (('mountPoint', '/boot'),): [(1689585060000, 4.85)], 
                   }
               }
           }
       }
       ```
     
        - data数据内部介绍

        > 第一层为云实例id，如`MRS-MN-02`
        >
        > 第二层为监控指标key，如`freeSpace`
        >
        > 第三层
        >
        > ​		如无维度，则value为时间戳与值的元组列表
        > 								
        > ​		如有维度，第三层为
        > 								
        > ​		key为维度key和value的嵌套元组，支持多维度，每个维度为一个元组
        > 								
        > ​		value为时间戳与值的元组列表
        > 								
        > ​		单维度`(('mountPoint', '/'),): [(1689585060000, 14.66)]`
        > 								
        > ​		多维度`(('mountPoint', '/'),('xx','1')): [(1689585060000, 14.66)]`



### 依赖

- requirements.txt填写额外依赖包，如xxsdk等

- 该版本暂不支持依赖包的直接引入，可重新生成docker镜像构建。

