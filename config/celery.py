from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Celery yapılandırmasını Django'nun ayarlarından al
app.config_from_object('django.conf:settings', namespace='CELERY')

# Görevlerin otomatik olarak bulunmasını sağlar
app.autodiscover_tasks()