import os
import stat
from web.models import FileInfo
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime
from django.urls import reverse
from django.shortcuts import get_object_or_404
from web.forms.file import FileModelForm  # 导入表单类


@csrf_exempt
def file(request, project_id):
    if request.method == "GET":
        queryset = FileInfo.objects.filter(updated_by=request.tracer.user).all()
        return render(request, 'file.html', {"queryset": queryset})

    # POST 请求处理
    mobile_phone = request.tracer.user.mobile_phone  # 获取用户的手机号码
    folder_name = datetime.now().strftime("%Y%m%d%H%M%S")  # 创建文件夹名称

    # 创建用户的文件夹路径
    user_directory = os.path.join(settings.MEDIA_ROOT, mobile_phone, folder_name)

    # 检查用户文件夹是否存在，如果不存在则创建
    os.makedirs(user_directory, exist_ok=True)

    # 获取上传的文件
    files = request.FILES.getlist('uploadFile')  # 获取上传的文件
    total_file_size = 0  # 初始化总文件大小

    for file in files:
        fs = FileSystemStorage(location=user_directory)  # 指定存储位置为用户的子文件夹
        fs.save(file.name, file)  # 保存文件
        total_file_size += file.size  # 累加文件大小

    # 创建 FileInfo 实例并保存到数据库
    file_info = FileInfo(
        name=folder_name,  # 使用文件夹名称
        file_size=total_file_size,  # 设置总文件大小
        updated_by=request.tracer.user,  # 设置更新者
        updated_at=datetime.now()  # 使用时区感知的时间
    )

    # 保存到数据库
    file_info.save()  # 保存实例
    return JsonResponse({'message': 'Files uploaded successfully!'}, status=200)


@csrf_exempt
def file_delete(request, project_id, file_id):
    mobile_phone = request.tracer.user.mobile_phone  # 假设您能从请求中获取用户手机号码
    file_queryset = FileInfo.objects.filter(id=file_id).first()
    file_name = file_queryset.name

    file_path = os.path.join(settings.MEDIA_ROOT, mobile_phone, file_name)

    # 检查文件是否存在并删除
    if os.path.exists(file_path):
        # os.chmod(file_path, stat.S_IWRITE)
        # os.remove(file_path)  # 删除文件
        FileInfo.objects.filter(id=file_id).delete()  # 从数据库中删除记录

    url = reverse('manage:file', kwargs={'project_id': project_id})
    return redirect(url)
