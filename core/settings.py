import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8080
    env: str = "prod"
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logging_dir = os.path.join(base_dir, "logs")
    logging_level = "INFO"
    db_url: str = "sqlite:///./dev.db"
    secret_key = b"78f40f2cffeee727a4b892dgas"

    # celery_broker: str = "sqla+sqlite:///celery.db"
    celery_broker: str = "redis://:@localhost:6379/0"
    celery_backend: str = "redis://:@localhost:6379/13"
    celery_result_expires: int = 60 * 60 * 24 * 7  # 默认7天
    playbook_path = os.path.join(base_dir, "asserts/playbooks")
    private_data_path = os.path.join(base_dir, "ansible_data")
    inventory_path = os.path.join(base_dir, "inventory")
    ansible_library = os.path.join(base_dir, "ansible_plugins")
    ansible_module_utils = os.path.join(ansible_library, "module_utils")
    redis_url: str = "redis://:123456@localhost?db=11"
    server_path: str = "server"
    driver_path: str = "core/driver"
    ansible_handler_path: str = "core/driver/ansible/handlers"

    push_gateway_url: str = "http://10.10.10.10:9001"

    vault_url: str = "http://vault.example.com"

    vault_token: str = "hvs.1BIQTBf81injy1FdExio6gkj"

    max_thread_num: int = 16

    class Config:
        env_file = ".env"


settings = Settings()
