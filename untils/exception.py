# -*- coding: utf-8 -*-
# author：王勇
import time

from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details, ErrorDetail
from django.utils.translation import gettext_lazy as _
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict



class throttle_exception(APIException):
    default_detail = '请求过于频繁'
    default_code = 429

    def __init__(self, message=None, code=429, **kwargs):
        self.message = message if message != None else  self.default_detail
        self.code = code
        tips = {"code": self.code, "message": self.message}
        tips.update(kwargs)
        self.detail = self._get_error_details(tips, default_code=status.HTTP_429_TOO_MANY_REQUESTS)

    def _get_error_details(self ,data, default_code=None):
        """
        Descend into a nested data structure, forcing any
        lazy translation strings or strings into `ErrorDetail`.
        """
        if isinstance(data, (list, tuple)):
            ret = [
                self._get_error_details(item, default_code) for item in data
            ]
            if isinstance(data, ReturnList):
                return ReturnList(ret, serializer=data.serializer)
            return ret
        elif isinstance(data, dict):
            ret = {
                key: self._get_error_details(value, default_code)
                for key, value in data.items()
            }
            if isinstance(data, ReturnDict):
                return ReturnDict(ret, serializer=data.serializer)
            return ret

        return data






