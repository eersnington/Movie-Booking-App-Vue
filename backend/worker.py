# pyright: reportMissingImports=false, reportMissingModuleSource=false

from celery import Celery

celery_config = {
    'broker_url': 'redis://localhost:6379/1',
    'result_backend': 'redis://localhost:6379/2'
}

celery_app = Celery()
celery_app.config_from_object(celery_config)

with celery_app.connection() as connection:
    celery_app.control.purge()
