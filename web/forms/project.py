#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from web.forms.widgets import ColorSelect
from web.forms.BootStrapForm import BootStrapForm
from web import models


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    # desc = forms.CharField(widget=forms.Textarea(attrs={'xx': 123}))
    bootStrap_class_exclude = ['color']
    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea,
            'color': ColorSelect(attrs={"class": 'color-radio'})
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        """ 项目校验 """
        name = self.cleaned_data['name']
        # 1. 当前用户是否已创建过此项目(项目名是否已存在)？
        exists = models.Project.objects.filter(name=name, creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError('项目名已存在')

        # 2. 当前用户是否还有额度进行创建项目？
        # 最多创建N个项目
        # self.request.tracer.price_policy.project_num

        # 现在已创建多少项目？
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()

        if count >= self.request.tracer.price_policy.project_num:
            raise ValidationError('项目个数超限，请购买套餐')

        return name
