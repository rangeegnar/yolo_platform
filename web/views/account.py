"""
用户账户相关功能:注册,短信,登录,注销
"""

import uuid
import datetime
from django.shortcuts import render, redirect
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from web import models
from django.db.models import Q



def register(request):
    """注册"""
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # 写入数据库(密码是密文)
        instance = form.save()

        # 创建交易记录
        police_object = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=police_object,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now()
        )

        return JsonResponse({"status": True, 'data': '/login/'})
    else:
        print(form.errors)
        return JsonResponse({"status": False, 'error': form.errors})


def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    """验证码登录"""
    if request.method == "GET":
        form = LoginSMSForm()
        return render(request, "login_sms.html", {"form": form})
    print(request.POST)
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        # 用户输入正确，登录成功
        mobile_phone = form.cleaned_data.get('mobile_phone')
        # 写入session
        print(request.POST)
        user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        request.session['user_id'] = user_object.id
        request.session['user_name'] = user_object.username
        request.session.set_expiry(60 * 60 * 24 * 14)

        return JsonResponse({"status": True, "data": "/index/"})

    return JsonResponse({"status": False, "error": form.errors})


def login(request):
    """用户名和密码"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user_object = models.UserInfo.objects.filter(
            Q(username=username) | Q(email=username) | Q(mobile_phone=username)
        ).filter(password=password).first()
        if not user_object:
            form.add_error('password', '用户名或密码错误')
            return JsonResponse({"status": False, "error": form.errors})
        else:
            request.session['user_id'] = user_object.id
            request.session['user_name'] = user_object.username
            request.session.set_expiry(60 * 60 * 24 * 14)
            return JsonResponse({"status": True, "data": "/index/"})

    return JsonResponse({"status": False, "error": form.errors})


def logout(request):
    request.session.flush()
    return redirect('index')