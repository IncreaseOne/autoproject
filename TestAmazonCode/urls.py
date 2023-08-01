# -*- coding: utf-8 -*-
# author：王勇

from django.contrib import admin
from django.urls import path, include
from .views import AmazonWebSite
urlpatterns = [
    path('testCode/', AmazonWebSite.as_view())
]
