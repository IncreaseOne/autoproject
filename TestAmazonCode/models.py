from django.db import models

# Create your models here.

from django import forms



class codeForm(forms.Form):
    goods_url = forms.URLField(error_messages={"invalid": "url数据格式不正确", 'required': "网址未传入"})
    code = forms.FloatField(error_messages={"required": "折扣码未传入"})