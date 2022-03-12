from django.shortcuts import render
from .models import Profile


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
