"""
WSGI config for AutoTestCode project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import asyncio
import os
import re
import time

import schedule
from django.core.wsgi import get_wsgi_application

from FacebookScreenshot.facebookplaywright import AutoScreenshot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoTestCode.settings')

application = get_wsgi_application()
import asyncio

from apscheduler.schedulers.background import  BackgroundScheduler

from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events

from FacebookScreenshot.facebookplaywright import AutoScreenshot

scheduler = BackgroundScheduler()
from AutoTestCode.settings import BASE_DIR

def remove_log():
    import os

    log_dir = r"{}/log".format(BASE_DIR)
    trace_dir = r"{}/trace".format(BASE_DIR)
    log_files = os.listdir(path=log_dir)
    trace_files = os.listdir(path=trace_dir)
    for i in log_files:
        if i.find("init") == -1:
            log_path = os.path.join(log_dir, i)
            log_file_create_time = os.path.getctime(log_path)
            if time.time() - log_file_create_time > 24 * 3600 * 10:
                os.remove(log_path)

    for i in trace_files:
        if i.find("init") == -1:
            trace_path = os.path.join(trace_dir, i)
            trace_file_create_time = os.path.getctime(trace_path)
            if time.time() - trace_file_create_time > 24 * 3600 * 10:
                os.remove(trace_path)

def login_facebook():
    screen_shot = AutoScreenshot()
    asyncio.run(screen_shot.start_login())

scheduler.add_job(func=login_facebook, trigger="interval", minutes=2880)
scheduler.add_job(func=remove_log, trigger="interval", minutes=60 * 24 * 5)
scheduler.start()


