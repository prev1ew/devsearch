from django.shortcuts import render, redirect
from .models import Project, Tag
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from .utils import search_projects


def projects(request):
    projects_data, search_query = search_projects(request)
    context = {'projects': projects_data,
               'search_query': search_query}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    tags = project_obj.tags.all()
    context = {'project': project_obj,
               'tags': tags}
    return render(request, 'projects/single_project.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            curr_project = form.save(commit=False)
            curr_project.owner = profile
            curr_project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    curr_project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=curr_project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=curr_project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    curr_project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        curr_project.delete()
        return redirect('account')

    context = {'object': curr_project}
    return render(request, 'delete_template.html', context)
