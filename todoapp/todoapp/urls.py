from django.contrib import admin
from django.urls import path, include
from tasks.views import index, LoginView, LogoutView, TaskDetailsView, TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('task_details/<int:pk>/', TaskDetailsView.as_view(), name='task_details'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('task_create', TaskCreateView.as_view(), name='task_create'),
    path('task_edit/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('task_details/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('task_details/<int:pk>/complete', TaskCompleteView.as_view(), name='task_complete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
