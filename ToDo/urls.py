"""
URL configuration for ToDo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from Task_Manager.views import *

urlpatterns = [

    path('admin/', admin.site.urls),

    path('Task_manager/home/',Home_View.as_view(),name='home'),
    path('Task_manager/signup/',User_SignUp_View.as_view(),name='signup'),
    path('Task_manager/login/',User_login_view.as_view(),name='login'),
    path('Task_manager/user_page/',Userpage_View.as_view(),name='userpage'),
    path('Task_manager/taskadd/',TaskAdd_view.as_view(),name='task_add'),
    path('Task_manager/forgot/',Forgot_View.as_view(),name='forgot'),
    path('Task_manager/logout/',Logout_View.as_view(),name='logout'),

    path('Task_manager/delete/<int:pk>',TaskDeleteView.as_view(),name='delete'),
    path('Task_manager/update/<int:pk>',TaskUpdate_view.as_view(),name='update'), 
    path('Task_manager/complete/<int:pk>',Task_complete_view.as_view(),name='complete'),
    path('Task_manager/task_progress/',Task_progress_view.as_view(),name='progress'),

    path('Task_manager/taskview/<int:pk>',TaskSelectView.as_view())
]
