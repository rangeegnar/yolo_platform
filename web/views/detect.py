import os
from tracer import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from web.ultralytics_main.A_demo.detect_try_user import detect_try_, get_unique_file_name
from django.http import JsonResponse
from web.models import FileInfo
from datetime import datetime


def detect(request, project_id):
    if request.method == "GET":
        return render(request, 'detect.html')


@csrf_exempt
def detect_try(request, project_id):
    if request.method == 'POST':
        image = request.FILES.get('image')
        threshold = request.POST.get('threshold')
        user_directory = os.path.join(settings.MEDIA_ROOT, request.tracer.user.mobile_phone)
        image_path = FileInfo.objects.filter(updated_by=request.tracer.user.id, name=image.name).first().file_path
        # print(image_path)
        if image_path and threshold:
            threshold = float(threshold)

            file_name, file_extension = os.path.splitext(image.name)
            new_image_name, new_image_path = get_unique_file_name(user_directory, file_name, file_extension)

            detect_try_(image_path, threshold, new_image_path)
            print(new_image_path)
            file_info = FileInfo(
                name=new_image_name,
                file_size=image.size,  # 文件大小
                updated_by=request.tracer.user,  # 文件创建者
                updated_at=datetime.now(),  # 使用时区感知的时间
                file_type=2,
                file_path=new_image_path
            )
            file_info.save()  # 保存到数据库
            return JsonResponse({'status': 'success', 'data': new_image_path})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing image or threshold.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
