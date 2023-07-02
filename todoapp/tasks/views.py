from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import LoginForm
from .models import Task

# Create your views here.
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

@login_required
def task_list(request):
    tasks = Task.objects.all()
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