from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_projects(request, projects_data, result):
    page = request.GET.get("page")
    try:
        page = int(page)
    except:
        page = 1

    paginator = Paginator(projects_data, result)

    try:
        projects_data = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects_data = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects_data = paginator.page(page)

    left_index = int((page - 4))

    if left_index < 1:
        left_index = 1

    right_index = int((page + 5))

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, projects_data


def search_projects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    projects_data = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return projects_data, search_query
