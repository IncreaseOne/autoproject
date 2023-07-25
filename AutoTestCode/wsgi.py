"""
WSGI config for AutoTestCode project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import asyncio
import os

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




def login_facebook():
    screen_shot = AutoScreenshot(code=None)
    asyncio.run(screen_shot.start_login())

scheduler.add_job(func=login_facebook, trigger="interval", minutes=2880)

scheduler.start()