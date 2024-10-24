from django.shortcuts import render

def file(request, project_id):
    return render(request, 'file.html')
