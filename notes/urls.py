"""
URL configuration for notes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', app_views.signup, name='signup'),
    path('profile/', app_views.user_profile, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='app/password_change.html',
        success_url='/password_change_done/'
    ), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/password_change_done.html'
    ), name='password_change_done'),
]
