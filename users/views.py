from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import User
from .forms import CustomUserCreation, ProfileForm, SkillForm
from django.contrib.auth.decorators import login_required


def profiles(request):
    profiles_data = Profile.objects.all()
    context = {'profiles': profiles_data}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')

    content = {'profile': profile,
               'top_skills': top_skills,
               'other_skills': other_skills}
    return render(request, 'users/user-profile.html', content)


def login_user(request):
    page = 'login'
    content = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username non-exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Username or passwd is incorrect')

    return render(request, 'users/login_register.html', content)


def logout_user(request):
    logout(request)
    messages.info(request, 'User was successfully logged out')
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreation()

    if request.method == 'POST':
        form = CustomUserCreation(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')

            login(request, user)
            return redirect('account')

        else:
            messages.error(request, 'An error was occurred during registration')

    content = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', content)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    content = {'profile': profile,
               'skills': skills,
               'projects': projects
               }
    return render(request, 'users/account.html', content)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    content = {'form': form}
    return render(request, 'users/profile_form.html', content)


@login_required(login_url="login")
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            curr_skill = form.save(commit=False)
            curr_skill.owner = profile
            curr_skill.save()
            messages.success(request, 'Skill was added successfully')
            return redirect('account')

    content = {'form': form}
    return render(request, 'users/skill_form.html', content)


@login_required(login_url="login")
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            # curr_skill = form.save(commit=False)
            # curr_skill.owner = profile
            # curr_skill.save()
            form.save()
            messages.success(request, 'Skill was updated')
            return redirect('account')

    content = {'form': form}
    return render(request, 'users/skill_form.html', content)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    content = {'object': skill}
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted')
        return redirect('account')
    return render(request, 'delete_template.html', content)
