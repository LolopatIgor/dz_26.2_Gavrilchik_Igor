import os
from celery import Celery

# Указываем, какой файл настроек Django использовать
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study.settings')

app = Celery('project')

# Настройки Celery берутся из настроек Django с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи в файлах tasks.py
app.autodiscover_tasks()