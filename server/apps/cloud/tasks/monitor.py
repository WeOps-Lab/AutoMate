import asyncio

from core.celery_app import celery_app
from core.driver.cmp.cmp_driver import CMPDriver
from core.logger import cmp_logger as logger
from core.pusher import prom_pusher
from core.settings import settings


def get_push_msg(metric, metric_value, timestamp, resource_id, resource_mapping, dims=None):
    dims = dims or []
    template = (
        timestamp,
        metric,
        {
            "bk_obj_id": resource_mapping[resource_id]["bk_obj_id"],
            "bk_inst_id": str(resource_mapping[resource_id]["bk_inst_id"]),
            "bk_inst_name": resource_mapping[resource_id]["bk_inst_name"],
            "bk_biz_id": str(resource_mapping[resource_id]["bk_biz_id"]),
            "instanceId": str(resource_id),
            "protocol": "cloud",
            "source": "automate",
        },
        metric_value,
    )
    for dim_key, dim_value in dims:
        template[2].update({dim_key: dim_value})
    return template


def parse_monitor_data(monitor_data, resource_mapping):
    msg_list = []
    for resource_id, metric_data in monitor_data.items():
        for metric, metric_list in metric_data.items():
            if isinstance(metric_list, dict):
                # 如果是dict,则存在维度数据
                for dims, _metric_list in metric_list.items():
                    if not metric_list:
                        continue
                    # 按60s来取点,取最后一个点.(如3:00-3:05 period=300,则取3.05的点)
                    try:
                        timestamp, metric_value = _metric_list[-1]
                    except Exception:
                        logger.exception(
                            f"[get_and_push_monitor] Error:metric parse error "
                            f"resource_id:{resource_id},metric:{metric},metric_list:{_metric_list}"
                        )
                        continue
                    msg = get_push_msg(metric, metric_value, timestamp, resource_id, resource_mapping, dims)
                    msg_list.append(msg)
            else:
                if not metric_list:
                    continue
                    # 按60s来取点,取最后一个点.(如3:00-3:05 period=300,则取3.05的点)
                try:
                    timestamp, metric_value = metric_list[-1]
                    if len(str(timestamp)) == 10:
                        timestamp = timestamp * 1000
                except Exception:
                    logger.exception(
                        f"[get_and_push_monitor] Error:metric parse error "
                        f"resource_id:{resource_id},metric:{metric},metric_list:{metric_list}"
                    )
                    continue
                msg = get_push_msg(metric, metric_value, timestamp, resource_id, resource_mapping)
                msg_list.append(msg)
    return msg_list


@celery_app.task(bind=True, name="get_and_push_monitor")
def get_and_push_monitor(
    self,
    account,
    password,
    cloud_type,
    resources,
    host,
    start_time,
    end_time,
    region=None,
    period=300,
    metrics=None,
    debug=False,
    **kwargs,
):
    resource_str = ",".join([i["resource_id"] for i in resources])
    resource_mapping = {i["resource_id"]: i for i in resources}
    region = region or None
    cmp_driver = CMPDriver(
        account=account, password=password, region=region, host=host, cloud_type=cloud_type, project_id=None
    )
    task_id = self.request.id
    logger.info(
        f"[get_and_push_monitor] start, task_id:{task_id};"
        f"cloud_type:{cloud_type}; resources:{resource_str}; period:{period} start_time:{start_time}; "
        f"host:{host};end_time:{end_time};metrics:{metrics}"
    )

    monitor_data = cmp_driver.get_weops_monitor_data(
        resourceId=resource_str,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Metrics=metrics or [],
        context={"resources": resources},
    )

    logger.info(
        f"[get_and_push_monitor] start, task_id:{task_id};"
        f"cloud_type:{cloud_type}; resources:{resource_str}; period:{period} start_time:{start_time}; "
        f"host:{host};end_time:{end_time};metrics:{metrics}"
    )
    if not monitor_data["result"]:
        logger.warning(
            f"[get_and_push_monitor] Error:get monitor data error ," f"task_id:{task_id};{monitor_data['message']}"
        )
        return
    monitor_data = monitor_data["data"]

    try:
        metric_list = parse_monitor_data(monitor_data, resource_mapping)
    except Exception:
        logger.exception(
            f"[get_and_push_monitor] Error:parse monitor data error ,"
            f"task_id:{task_id};monitor_data:{monitor_data}; resource_mapping:{resource_mapping}"
        )
        return
    logger.info("-----", metric_list, "-----")
    if debug:
        return metric_list
    coroutine = prom_pusher.mpush(metric_list)
    count = asyncio.get_event_loop().run_until_complete(coroutine)
    logger.info(
        f"[get_and_push_monitor] success:push monitor data to prometheus "
        f"task_id:{task_id};url:{settings.prometheus_rw_url};success_count:{count}"
    )
