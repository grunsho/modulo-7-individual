from django.contrib import admin
from django.urls import path, include
from tasks.views import index, LoginView, LogoutView, TaskDetailsView, TaskListView, TaskCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('task_details/<int:pk>/', TaskDetailsView.as_view(), name='task_details'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('task_create', TaskCreateView.as_view(), name='task_create'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
