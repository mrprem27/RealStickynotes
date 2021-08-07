from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("add",views.add_task,name="add_task"),
    path("mark_task",views.mark_task,name="mark_task"),
    path("del_task",views.del_task,name="del_task"),
    path("open",views.open,name="open"),
    path("search_task",views.search_task,name="search_task"),
    path("signup",views.add_user,name="signup"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("edit",views.edit,name="edit"),
]
