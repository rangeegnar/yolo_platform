from django.shortcuts import render


def settings(request, project_id):

    return render(request, 'setting.html')