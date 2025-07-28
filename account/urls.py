from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.account, name='account'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path("validate-field/", views.validate_register_field, name="validate_field"),
    path('logout/', views.logout_view, name="logout"),
    path('delete-account/', views.delete_account, name='delete_account'),
]
