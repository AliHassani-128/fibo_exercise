from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from fib.models import Fibonacci


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibo_celery.settings')

app = Celery('fibo_celery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

logger = get_task_logger(__name__)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s(), name='add every 10')


@app.task
def test():
    fibo = Fibonacci.objects.all().order_by('-id')[:2]
    if len(fibo) >= 2 :
        result = fibo[0].value + fibo[1].value
        index = fibo[1].index + 1
        Fibonacci.objects.create(index=index, value=result)
        index += 1
        result += fibo[1].value
        Fibonacci.objects.create(index=index, value=result)

    else:
        Fibonacci.objects.create(index=1,value=1)
        Fibonacci.objects.create(index=2, value=1)
