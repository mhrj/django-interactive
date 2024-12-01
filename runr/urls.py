from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run-r-script/', views.run_r_script, name='run_r_script'),
]