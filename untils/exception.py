# -*- coding: utf-8 -*-
# author：王勇
import time

from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details
from django.utils.translation import gettext_lazy as _

class throttle_exception(APIException):
    default_detail = _('请求过于频繁')
    default_code = 429

    def __init__(self, message=None, code=None):
        self.message = message if message != None else  message
        self.code = code if code != None else code
        self.detail = _get_error_details({"code": self.code, "message": self.message}, default_code=status.HTTP_429_TOO_MANY_REQUESTS)





