from django.shortcuts import render, redirect
from .models import Project
from django.http import HttpResponse
from .forms import ProjectForm


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


def create_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def update_project(request, pk):
    curr_project = Project.objects.get(id=pk)
    form = ProjectForm(instance=curr_project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=curr_project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def delete_project(request, pk):
    curr_project = Project.objects.get(id=pk)

    if request.method == 'POST':
        curr_project.delete()
        return redirect('projects')

    context = {'object': curr_project}
    return render(request, 'projects/delete_template.html', context)
