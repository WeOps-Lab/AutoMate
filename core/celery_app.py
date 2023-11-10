from celery import Celery

from core.init import init_service

celery_app = Celery(__name__)

celery_app.config_from_object("core.celeryconfig")

init_service()

if __name__ == "__main__":
    celery_app.start()
    # celery -A server.core.celery_app worker -l info
