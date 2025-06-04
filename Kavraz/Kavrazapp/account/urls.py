from django.urls import path
from . import views

urlpatterns = [
    path('', views.account),
    path('account/', views.account),
    path('login/', views.login_view),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name="logout"),
]
