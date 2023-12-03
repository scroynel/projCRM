from django.urls import path

from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.teams_list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.teams_edit, name='edit'),
    path('<int:pk>/activate/', views.teams_activate, name='activate'),
]