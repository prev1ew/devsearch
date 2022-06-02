from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import User
from .forms import CustomUserCreation


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
            return redirect('profiles')
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
            return redirect('profiles')

        else:
            messages.error(request, 'An error was occurred during registration')

    content = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', content)
