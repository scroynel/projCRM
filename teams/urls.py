from django.urls import path

from . import views

app_name = 'teams'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.teams_edit, name='edit'),
]