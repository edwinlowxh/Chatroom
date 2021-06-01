from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('login', views.login, name = "login"),
    path('register', views.register, name = 'register'),
    path('Chat', views.chat, name = "chat"),
    path('new_group', views.new_group, name = "new_group"),
    path('search_users', views.search_users, name = "search_users")
]
