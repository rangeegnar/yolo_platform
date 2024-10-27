import os
from tracer import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from web.ultralytics_main.A_demo.detect_try_user import detect_try_
from django.http import JsonResponse
from web.models import FileInfo, Pretrain_model
from datetime import datetime
from utils.avoid_same_name import detect_get_unique_file_name


def detect(request, project_id):
    if request.method == "GET":
        files = FileInfo.objects.filter(file_type=2, updated_by=request.tracer.user.id)
        pretrains = Pretrain_model.objects.all()
        return render(request, 'detect.html', {'files': files, 'pretrains': pretrains})


@csrf_exempt
def detect_try(request, project_id):
    if request.method == 'POST':

        file_id = request.POST.get('file_id')
        threshold = request.POST.get('threshold')
        pretrain = request.POST.get('pretrain')

        file_object = FileInfo.objects.filter(id=file_id, updated_by=request.tracer.user.id).first()
        user_directory = os.path.join(settings.MEDIA_ROOT, request.tracer.user.mobile_phone)

        image_video_path = FileInfo.objects.filter(updated_by=request.tracer.user.id,
                                                   name=file_object.name).first().file_path
        # print(image_path)
        if image_video_path and threshold:
            threshold = float(threshold)

            file_name, file_extension = os.path.splitext(file_object.name)
            new_image_video_name, new_image_video_path = detect_get_unique_file_name(user_directory, file_name,
                                                                                     file_extension)
            new_image_video_path = new_image_video_path.replace('\\', '/')

            detect_try_(image_video_path, threshold, new_image_video_path, pretrain)

            file_info = FileInfo(
                name=new_image_video_name,
                file_size=file_object.file_size,  # 文件大小
                updated_by=request.tracer.user,  # 文件创建者
                updated_at=datetime.now(),  # 使用时区感知的时间
                file_type=2,
                file_path=new_image_video_path.replace('\\', '/'),
                media_url=f"{settings.MEDIA_URL}{request.tracer.user.mobile_phone}/{new_image_video_name}",
            )
            file_info.save()  # 保存到数据库
            print(new_image_video_path)
            return JsonResponse({'status': True, 'data': file_info.media_url, 'where': file_info.name})
        else:
            return JsonResponse({'status': False, 'message': 'Missing image or threshold.'})
    return JsonResponse({'status': False, 'message': 'Invalid request method.'})
