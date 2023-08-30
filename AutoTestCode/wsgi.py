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

    log_dir = f"{BASE_DIR}\log"
    list_files = os.listdir(path=log_dir)

    for i in list_files:
        re_date = re.search("(?P<date>[\d|-]*).log", i)
        if re_date != None:
            date = re_date.group("date")
            timestamp = time.mktime(time.strptime(date, "%Y-%m-%d"))
            if time.time() - timestamp > 24 * 3600 * 10:
                os.remove(os.path.join(log_dir, i))


def login_facebook():
    screen_shot = AutoScreenshot()
    asyncio.run(screen_shot.start_login())

scheduler.add_job(func=login_facebook, trigger="interval", minutes=2880)
scheduler.add_job(func=remove_log, trigger="interval", minutes=60*24*5)
scheduler.start()