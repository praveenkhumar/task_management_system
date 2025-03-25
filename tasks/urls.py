from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api

app_name = 'tasks'

router = DefaultRouter()
router.register(r'tasks', api.TaskViewSet, basename='task-api')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/update/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    
    # API URLs
    path('api/', include(router.urls)),
]