import os
import django

# 设置设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracer.settings')

# 初始化 Django
django.setup()


from web import models

def run():
    exists = models.PricePolicy.objects.filter(category=1, )
    if not exists:
        models.PricePolicy.objects.create(
            category=1,
            title='个人免费版',
            price=0,
            project_num=3,
            project_member=2,
            project_space=20,
            per_file_size=5,
        )


if __name__ == '__main__':
    run()
