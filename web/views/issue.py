from django.shortcuts import render


def issue(request, project_id):
    return render(request, 'issue.html')