from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .forms import LoginForm, TaskForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, Comment
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


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('index')


class TaskDetailsView(LoginRequiredMixin, View):
    template_name: 'task_details.html'
    
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskDetailsView(instance = task)
        commentform = CommentForm
        comments = Comment.objects.filter(task_id=task.id)
        print(comments)
        context = {'task': task,
                    'form': form,
                    'commentform': commentform,
                    'comments': comments}
        return render(request, 'task_details.html', context)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        commentform = CommentForm(data=request.POST)
        comments = Comment.objects.filter(task_id=task.id)
        if commentform.is_valid():
            new_comment = commentform.save(commit=False)
            new_comment.task_id = task.id
            new_comment.save()
        context = {
            'task': task,
                'commentform': commentform,
                'comments': comments,
                'new_comment': new_comment
        }
        
        return render(request, 'task_details.html', context)


class TaskListView(LoginRequiredMixin, View):
    model = Task
    template_name = 'task_list.html'
    
    def get(self, request):
        tasks = Task.objects.filter(user=request.user).exclude(status='Completada').order_by('due_date')
        context = {'tasks': tasks}
        return render(request, self.template_name, context)

    def post(self, request):
        filter_by = request.POST.get('filter_by')
        tasks = Task.objects.order_by('due_date').filter(status=filter_by)
        context = {'tasks': tasks}
        return render(request, self.template_name, context)


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

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