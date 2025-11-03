from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('signup/', views.Signup, name='signup'),
    path("login/", views.Login, name="login"),
    path("profile/", views.Profile, name="profile"),
    path("requests/", views.Requests, name="requests"),
    path('add_request/', views.add_request, name='addRequest'),
    path('settings/', views.settings_page, name='settings'),
]