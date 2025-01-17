from django.urls import path, include
from web.views import account, home, project, wiki, dashboard, detect, statistics, file, setting
from django.conf.urls.static import static
from tracer import settings

urlpatterns = [
    # 用户相关的 URL
    path('register/', account.register, name='register'),
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/', account.login, name='login'),
    path('index/', home.index, name='index'),
    path('send/sms/', account.send_sms, name='send_sms'),
    path('logout/', account.logout, name='logout'),  # 修正为 logout

    # 项目相关的 URL
    path('project/list/', project.project_list, name='project_list'),
    path('project/star/<str:project_type>/<int:project_id>/', project.project_star, name='project_star'),
    path('project/unstar/<str:project_type>/<int:project_id>/', project.project_unstar, name='project_unstar'),

    # 项目管理相关的 URL
    path('manage/<int:project_id>/', include(([
        path('dashboard/', dashboard.dashboard, name='dashboard'),

        path('detect/detect', detect.detect, name='detect'),
        path('detect/detectry/', detect.detect_try, name='detectry'),

        path('statistics/', statistics.statistics, name='statistics'),

        path('file/', file.file, name='file'),
        path('file/delete/<int:file_id>/', file.file_delete, name='file_delete'),
        path('file/edit/<int:file_id>/', file.file_edit, name='file_edit'),
        path('file/detail/<int:file_id>/', file.file_detail, name='file_detail'),
        path('file/download/<int:file_id>/', file.file_download, name='file_download'),

        # Wiki 相关的 URL
        path('wiki/', wiki.wiki, name='wiki'),
        path('wiki/add/', wiki.wiki_add, name='wiki_add'),
        path('wiki/delete/<int:wiki_id>/', wiki.wiki_delete, name='wiki_delete'),
        path('wiki/edit/<int:wiki_id>/', wiki.wiki_edit, name='wiki_edit'),
        path('wiki/catalog/', wiki.wiki_catalog, name='wiki_catalog'),

        path('settings/', setting.settings, name='settings'),
    ], 'manage'), namespace='manage')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 添加媒体文件支持
urlpatterns += static(settings.PRETRAINED_MODELS_URL, document_root=settings.PRETRAINED_MODELS_ROOT)