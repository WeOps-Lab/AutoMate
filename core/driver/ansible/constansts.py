# 默认ansible 任务状态的redis超时时间
DEFAULT_ANSIBLE_RUNNER_MAX_TIMEOUT = 24 * 60 * 60

# Ansible runner Key
ANSIBLE_RUNNER_KEY = "ANSIBLE_RUNNER_{}"

# Default Async Handler
DEFAULT_HANDLER = "BaseHandler.finished_callback"

# prometheus Handler
PROMETHEUS_HANDLER = "PrometheusHandler.finished_callback"
