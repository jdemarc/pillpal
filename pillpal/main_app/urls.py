from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('main/', views.main, name='main'),
  path('prescriptions/', views.prescriptions_index, name='index'),
  path('prescriptions/<int:prescription_id>/', views.prescriptions_detail, name='detail'),
  path('prescriptions/create/', views.PrescriptionCreate.as_view(), name='prescriptions_create'),
  path('prescriptions/<int:pk>/update/', views.PrescriptionUpdate.as_view(), name='prescriptions_update'),
  path('prescriptions/<int:pk>/delete/', views.PrescriptionDelete.as_view(), name='prescriptions_delete'),
  path('accounts/signup/', views.signup, name='signup'),
]