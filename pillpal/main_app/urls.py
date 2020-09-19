from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('main/', views.main, name='main'),
  path('prescriptions/', views.prescriptions_index, name='index'),
  path('prescriptions/<int:prescription_id>/', views.prescriptions_detail, name='detail'),
  path('accounts/signup/', views.signup, name='signup'),
]