from accounts.views import delete_view, login_view, logout_view, register_view, update_view
from search_work_site.views import list_view
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('update/', update_view, name='update'),
    path('delete/', delete_view, name='delete')
]
