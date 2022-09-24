from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import SingUp
urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sing_up/', SingUp.as_view(), name='sig_up'),


]