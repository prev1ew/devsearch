from django.shortcuts import render
from .models import Project
from django.http import HttpResponse


def projects(request):

    projects_data = Project.objects.all()
    context = {'projects': projects_data}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    tags = project_obj.tags.all()
    context = {'project': project_obj,
               'tags': tags}
    return render(request, 'projects/single_project.html', context)
