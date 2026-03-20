from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.RABBITMQ_URL,
    backend=settings.redis_url    # Для хранения результатов (необязательно, но полезно)
)

# Автоматический поиск задач в папке worker
celery_app.autodiscover_tasks(["app.worker"])

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Kyiv",
    enable_utc=True,
    broker_transport_options={'max_retries': 3, 'interval_start': 0, 'interval_step': 0.2, 'interval_max': 0.5},
    result_backend_transport_options={'retry_policy': {'timeout': 2.0}},
    redis_backend_health_check_interval=5,
)