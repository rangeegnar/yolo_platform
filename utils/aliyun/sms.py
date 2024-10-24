#!/usr/bin/env python
# -*- coding:utf-8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.conf import settings
import json

# 创建AcsClient实例
client = AcsClient(settings.ALIYUN_ACCESS_KEY_ID, settings.ALIYUN_ACCESS_KEY_SECRET, 'cn-hangzhou')


def send_sms_single(phone_num, template_code, template_param_dict):
    """
    单条发送短信
    :param phone_num: 手机号
    :param template_code: 阿里云短信模板Code
    :param template_param_dict: 短信模板所需参数字典，例如: {'code': '888888'}
    :return: 阿里云返回的response或错误信息
    """
    # 确保 template_param_dict 是字典类型
    if isinstance(template_param_dict, set):
        template_param_dict = list(template_param_dict)  # 将集合转换为列表

    params = {
        "PhoneNumbers": phone_num,
        "SignName": settings.ALIYUN_SMS_SIGN,
        "TemplateCode": template_code,
        "TemplateParam": json.dumps(template_param_dict)  # 字典转JSON字符串
    }

    # 发送请求
    try:
        request = CommonRequest()
        request.set_method('POST')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        for key, value in params.items():
            request.add_query_param(key, value)

        response = client.do_action_with_exception(request)
        return response.decode('utf-8')  # 返回结果需要解码
    except Exception as e:
        return {'result': 1000, 'errmsg': f"网络异常发送失败: {str(e)}"}


def send_sms_multi(phone_num_list, template_code, param_list):
    """
    批量发送短信
    :param phone_num_list: 手机号列表
    :param template_code: 阿里云短信模板Code
    :param param_list: 短信模板所需参数列表，例如: [{'code': '888'}, {'code': '666'}]
    :return: 阿里云返回的response或错误信息
    """
    # 创建请求
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_version('2017-05-25')
    request.set_action_name('SendBatchSms')

    # 设置请求参数
    request.add_query_param('PhoneNumberJson', json.dumps(phone_num_list))
    request.add_query_param('SignNameJson', json.dumps([settings.ALIYUN_SMS_SIGN] * len(phone_num_list)))
    request.add_query_param('TemplateCode', template_code)
    request.add_query_param('TemplateParamJson', json.dumps(param_list))  # 参数列表必须为JSON格式

    # 发送请求
    try:
        response = client.do_action_with_exception(request)
        return response.decode('utf-8')
    except Exception as e:
        return {'result': 1000, 'errmsg': f"网络异常发送失败: {str(e)}"}
