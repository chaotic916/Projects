from django.urls import path
from . import views
from .forms import LoginForm
from django.contrib.auth import views as auth_views

app_name = 'mall'  # Namespace for URLs

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='mall/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]