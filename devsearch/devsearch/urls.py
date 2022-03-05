from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home_page(request):
    return HttpResponse('Home Page')


urlpatterns = [
    # path('', home_page),
    path('admin/', admin.site.urls),
    path('', include('projects.urls'))

]
