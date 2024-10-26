import os
from web.models import FileInfo
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime
from django.urls import reverse
import shutil
import zipfile
from utils.avoid_same_name import get_unique_file_name
from django.shortcuts import get_object_or_404
from web.forms.file import FileModelForm  # 导入表单类


@csrf_exempt
def file(request, project_id):
    if request.method == "GET":
        queryset = FileInfo.objects.filter(updated_by=request.tracer.user).all()
        return render(request, 'file.html', {"queryset": queryset})

    # POST 请求处理
    mobile_phone = request.tracer.user.mobile_phone  # 获取用户的手机号码
    # 获取上传的文件夹
    if request.FILES.getlist('uploadFile'):
        # 创建文件夹名称
        folder_name = datetime.now().strftime("%Y%m%d%H%M%S")
        # 创建用户的文件夹路径
        user_directory = os.path.join(settings.MEDIA_ROOT, mobile_phone, folder_name)
        # 检查用户文件夹是否存在，如果不存在则创建
        os.makedirs(user_directory, exist_ok=True)

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
            updated_at=datetime.now(),  # 使用时区感知的时间
            file_type=1,
            file_path=os.path.join(user_directory, folder_name).replace('\\', '/')
        )

        # 保存到数据库
        file_info.save()  # 保存实例
        return JsonResponse({'message': 'Files uploaded successfully!'}, status=200)
    else:
        files = request.FILES.getlist('uploadFile_only')  # 获取上传的单独文件

        # 创建用户的文件夹路径
        user_directory = os.path.join(settings.MEDIA_ROOT, mobile_phone)
        # 检查用户文件夹是否存在，如果不存在则创建
        os.makedirs(user_directory, exist_ok=True)

        for file in files:
            # 确保文件名唯一
            unique_file_name, unique_file_path = get_unique_file_name(user_directory, file.name)

            fs = FileSystemStorage(location=user_directory)  # 指定存储位置为用户的目录
            fs.save(unique_file_name, file)  # 保存文件

            # 创建 FileInfo 实例并保存到数据库
            file_info = FileInfo(
                name=unique_file_name,  # 使用文件名
                file_size=file.size,  # 设置单个文件大小
                updated_by=request.tracer.user,  # 设置更新者
                updated_at=datetime.now(),  # 使用时区感知的时间
                file_type=2,
                file_path=unique_file_path.replace('\\', '/')  # 保存新文件的路径
            )

            # 保存到数据库
            file_info.save()  # 保存实例

        return JsonResponse({'message': 'Single files uploaded successfully!'}, status=200)


@csrf_exempt
def file_delete(request, project_id, file_id):
    mobile_phone = request.tracer.user.mobile_phone  # 假设您能从请求中获取用户手机号码
    file_queryset = FileInfo.objects.filter(id=file_id).first()
    file_name = file_queryset.name
    file_type = file_queryset.file_type
    file_path = os.path.join(settings.MEDIA_ROOT, mobile_phone, file_name)

    # 检查文件是否存在并删除
    if os.path.exists(file_path):
        if file_type == 2:
            os.remove(file_path)  # 删除文件
        else:
            shutil.rmtree(file_path)  # 删除文件夹及其内容
    # 从数据库中删除记录
    FileInfo.objects.filter(id=file_id).delete()
    url = reverse('manage:file', kwargs={'project_id': project_id})
    return redirect(url)


@csrf_exempt
def file_edit(request, project_id, file_id):
    mobile_phone = request.tracer.user.mobile_phone  # 假设您能从请求中获取用户手机号码
    file_queryset = FileInfo.objects.filter(id=file_id).first()
    file_name = file_queryset.name

    file_path = os.path.join(settings.MEDIA_ROOT, mobile_phone, file_name)

    # # 检查文件是否存在并删除
    # if os.path.exists(file_path):
    #     # os.chmod(file_path, stat.S_IWRITE)
    #     # os.remove(file_path)  # 删除文件
    #     FileInfo.objects.filter(id=file_id).delete()  # 从数据库中删除记录

    url = reverse('manage:file', kwargs={'project_id': project_id})
    return redirect(url)


@csrf_exempt
def file_detail(request, project_id, file_id):
    folder_queryset = FileInfo.objects.filter(id=file_id).first()
    folder_name = folder_queryset.name
    folder_directory = os.path.join(settings.MEDIA_ROOT, request.tracer.user.mobile_phone, folder_name)
    detail_list = []
    if os.path.exists(folder_directory):
        for filename in os.listdir(folder_directory):
            file_path = os.path.join(folder_directory, filename)
            if os.path.isfile(file_path):  # 确保是文件
                detail_list.append(filename)  # 仅存储文件名
        return JsonResponse({'status': True, 'detail_list': detail_list})
    return JsonResponse({'status': False, 'message': '文件夹不存在或无法访问'})


@csrf_exempt
def file_download(request, project_id, file_id):
    if request.method == 'POST':
        # 假设有一个 File 模型来存储文件信息
        file_object = FileInfo.objects.filter(id=file_id, updated_by=request.tracer.user.id).first()
        file_name = file_object.name
        file_type = file_object.file_type

        to_file_path = request.POST.get('file_path')  # 下载到
        to_file_path = to_file_path.strip('"').replace("\\", "/")

        print(to_file_path)
        # 构建文件路径-源文件
        source_file_path = os.path.join(settings.MEDIA_ROOT, request.tracer.user.mobile_phone, file_name).replace('\\',
                                                                                                                  '/')
        print(source_file_path)
        if file_type == 2:
            # 检查源文件是否存在
            if os.path.exists(source_file_path):
                to_file_path = to_file_path + '/' + file_name
                # 将源文件内容写入到目标路径
                with open(source_file_path, 'rb') as source_file:
                    with open(to_file_path, 'wb') as target_file:
                        target_file.write(source_file.read())

                return JsonResponse({'status': True, 'message': '文件已成功下载到指定路径'})
        else:
            zip_file_path = os.path.join(to_file_path, f"{file_name}.zip")
            # 压缩文件夹
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # 遍历文件夹及其内容
                for root, dirs, files in os.walk(source_file_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # 添加文件到 ZIP
                        zip_file.write(file_path, os.path.relpath(file_path, source_file_path))
            return JsonResponse({'status': True, 'message': '文件夹已成功下载为 ZIP 文件', 'zip_file_path': zip_file_path})
        return JsonResponse({'status': False, 'message': '下载失败'}, status=404)
