"""search_work_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from search_work_service.views import redirect_to_home_page
from accounts.views import login_view
from search_work_site.views import VCreate, VDelete, VDetail, VList, VUpdate, list_view, view_detail
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', redirect_to_home_page),
    path('admin/', admin.site.urls),
    path('list/', list_view, name='list'),
    path('detail/<int:pk>/', VDetail.as_view(), name='detail'),
    path('create/', VCreate.as_view(), name='create'),
    path('update/<int:pk>/', VUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', VDelete.as_view(), name='delete'),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('home/', include('search_work_site.urls'))
]
