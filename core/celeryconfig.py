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

CELERY_IMPORTS = [
    "core.tasks",
    "server.apps.cloud.tasks.monitor",
]

# 队列设置
# CELERY_TASK_QUEUES = (  # 设置add队列,绑定routing_key
#     Queue('default', routing_key='default'),
#     Queue('email', routing_key='send_email'),
# )
#
# task_routes = {  # projq.tasks.add这个任务进去add队列并routeing_key为xue.add
#     'app.api.api_v1.tasks.emails.decoratorEmail': {
#         'queue': 'email',
#         'routing_key': 'send_email',
#     }
# }
