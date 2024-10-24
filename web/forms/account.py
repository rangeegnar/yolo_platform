import random
import json
import redis
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from utils.aliyun.sms import send_sms_single
from django_redis import get_redis_connection
from web.forms.BootStrapForm import BootStrapForm


class RegisterModelForm(BootStrapForm, forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(label='密码',
                               min_length=8,
                               max_length=64,
                               error_messages={
                                   'min_length': "密码长度不能小于8字符",
                                   "max_length": "密码长度不能大于64字符"
                               },
                               widget=forms.PasswordInput()
                               )
    confirm_password = forms.CharField(label='重复密码',
                                       min_length=8,
                                       max_length=64,
                                       error_messages={
                                           'min_length': "密码长度不能小于8字符",
                                           "max_length": "密码长度不能大于64字符"
                                       },
                                       widget=forms.PasswordInput()
                                       )
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']
        # fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)

    def clean_username(self):
        username = self.cleaned_data['username']
        exist = models.UserInfo.objects.filter(username=username).exists()
        if exist:
            raise ValidationError('用户名已存在')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # 可以加密,但我不想写
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("前后密码不一致")
        return confirm_password

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        exist = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exist:
            raise ValidationError('手机号已存在')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data.get('code')
        mobile_phone = self.cleaned_data.get('mobile_phone')
        # cleaned_data 对于每一个实体（username,email,...)只有验证成功才有对应的键和值，因此在输入相同手机号的时候，进行检测验证码的时候，会报错
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError("验证码失效或者未发送")

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code.strip():
            raise ValidationError('验证码错误')

        return code


# ModelForm与数据库有联系, 而Form不涉及存储
class SendSmsForm(forms.Form):
    # 这是第二步（检验格式是否正确）
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ])

    # 实例化会先执行init(), 使用views的东西
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # 第三步：检验mobile是否已经注册, register/login写错
    def clean_mobile_phone(self):
        """手机号检验的钩子"""
        # mobile_phone = self.cleaned_data['mobile_phone']代表已经完成基本认证（不空，格式正确）
        mobile_phone = self.cleaned_data['mobile_phone']

        # 短信模板错误
        tpl = self.request.GET.get('tpl')
        template_id = settings.ALIYUN_SMS_TEMPLATE.get(tpl)
        if not template_id:
            # self.add_error('mobile_phone', '短信模板错误')  会一直往下走
            raise ValidationError('短信模板错误')

        # 手机号已存在
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'register':
            if exists:
                raise ValidationError('手机号已存在')
        elif tpl == 'login':
            if not exists:
                raise ValidationError('手机号未注册')

        # 发短信
        code = random.randrange(1000, 9999)
        response = send_sms_single(mobile_phone, template_id, {'code': code})
        if isinstance(response, str):
            response_json = json.loads(response)  # 将字符串转换为字典
            if response_json.get('Code') != 'OK':
                error_message = response_json.get('Message', '短信发送失败，未知错误')
                raise ValidationError(f"短信发送失败: {error_message}")

        # 写入redis
        conn = get_redis_connection()
        try:
            conn.set(mobile_phone, code, ex=60)
        except redis.exceptions.ConnectionError as e:
            print(f"Redis connection error: {e}")

        return mobile_phone


class LoginSMSForm(BootStrapForm, forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ])
    code = forms.CharField(label='验证码')

    # clean_mobile_phone(self) 可以不用谢
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        exist = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if not exist:
            raise ValidationError("手机号不存在")
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data.get('code')
        mobile_phone = self.cleaned_data.get('mobile_phone')

        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError("验证码失效或未发送")
        redis_code_str = redis_code.decode('utf-8')
        if code.strip() != redis_code_str:
            raise ValidationError("验证码错误")

        return code


class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='用户名/邮箱/手机号')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
