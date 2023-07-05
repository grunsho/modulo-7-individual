from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.list import ListView
from .forms import LoginForm, TaskForm
from .models import Task
from django.db.models import Q

# Create your views here.
@user_passes_test(lambda user: not user.username, login_url='task_list', redirect_field_name=None)
def index(request):
    return render(request, 'index.html')

class LoginView(View):
    template_name = 'registration/login.html'
    
    def get(self, request):
        context = {'login_form': LoginForm()}
        return render(request, 'registration/login.html', context)

    def post(self, request):
        usuario = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if usuario is not None:
            login(request, usuario)
            return redirect('task_list')
        else:
            context = {"error": "Usuario no encontrado", 'login_form': LoginForm()}
            print(context)
            return render(request, 'registration/login.html', context)

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class TaskDetailsView(View):
    template_name: 'task_details.html'
    
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskDetailsView(instance = task)
        context = {'task': task,
                    'form': form}
        return render(request, 'task_details.html', context)

# class TaskListView(ListView):
#     model = Task
#     template_name = 'task_list.html'

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.order_by('due_date')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['status'] = self.get_queryset()
#         return context

@login_required
def task_list(request):  # sourcery skip: assign-if-exp, introduce-default-else
    if request.method == "POST":
        form = TaskForm(request.POST)
        status = request.POST.get('filter_by')
        print(status)
        tasks = Task.objects.all().filter(status=status)
    else:
        tasks = Task.objects.all().order_by('due_date')
        print('get')
        print(request.GET.get('filter_by'))
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        Task.objects.create(title=title)
        return redirect('task_list')
    return render(request, 'task_create.html')

@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        title = request.POST['title']
        completed = 'completed' in request.POST
        task.title = title
        task.completed = completed
        task.save()
        return redirect('task_list')
    return render(request, 'task_update.html', {'task': task})

@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_delete.html', {'task': task})