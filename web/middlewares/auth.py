from django.utils.deprecation import MiddlewareMixin
from web import models
from django.shortcuts import redirect
from django.conf import settings
import datetime


class Tracer(object):

    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """如果在用户已经login, 则在request中赋值"""
        request.tracer = Tracer()
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object

        # 白名单
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.tracer.user:
            return redirect('login')

        # 登录成功后
        _object = models.Transaction.objects.filter(user=user_object).order_by('-id').first()
        current_datatime = datetime.datetime.now()

        if _object and _object.end_datetime and _object.end_datetime < current_datatime:
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=0).first()

        request.tracer.price_policy = _object.price_policy


    def process_view(self, request, view, args, kwargs):

        # 判断URL是否用manager开头
        if not request.path_info.startswith('/manage/'):
            return
        # 是我创建的吗
        project_id = kwargs.get('project_id')
        project_object = models.Project.objects.filter(creator=request.tracer.user, id=project_id).first()
        if project_object:
            request.tracer.project = project_object
            return
        # 是我参与的项目吗
        project_user_object = models.ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_user_object:
            request.tracer.project = project_user_object.project
            return

        return redirect('project_list')



        
    