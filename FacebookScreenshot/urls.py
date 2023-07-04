# -*- coding: utf-8 -*-
# author：王勇

from django.contrib import admin
from django.urls import path, include

from FacebookScreenshot.views import Facebook

urlpatterns = [
    path('facebook', Facebook.as_view())
]
