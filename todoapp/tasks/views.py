from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import LoginForm, TaskForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, Comment, Tag
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
    form = TaskForm
    template_name = 'task_list.html'
    
    def get(self, request):  # sourcery skip: class-extract-method
        tasks = Task.objects.filter(user=request.user).exclude(status='Completa').order_by('due_date')
        tags = Tag.objects.all()
        context = {'tasks': tasks,
                    'tags': tags,
                    'form': self.form()}
        return render(request, self.template_name, context)

    def post(self, request):
        filter_by = request.POST.get('filter_by')
        if request.POST.get('tagfilter') is not None:
            tagname = request.POST.get('tagfilter')
            tagfilter = Tag.objects.get(name=tagname)
        else:
            tagfilter = None
        print(filter_by)
        print(tagfilter)
        tags = Tag.objects.all()

        if tagfilter is None:
            tasks = (
                Task.objects.filter(status=filter_by)
                .exclude(status="Completa")
                .order_by('due_date')
                if filter_by is not None
                else Task.objects.filter(user=request.user)
                .exclude(status='Completa')
                .order_by('due_date')
            )
        elif filter_by is not None:
            tasks = Task.objects.filter(status=filter_by, tag=tagfilter).exclude(status="Completa").order_by('due_date')
        else:
            tasks = Task.objects.filter(tag=tagfilter).exclude(status='Completada').order_by('due_date')
        context = {'tasks': tasks,
                    'tags': tags,
                    'form': self.form()}
        return render(request, self.template_name, context)


class TaskCreateView(LoginRequiredMixin, CreateView):
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


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')
    template_name = 'task_details.html'
    

class TaskCompleteView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    fields = {
        'status', 'completed'
    }
    template_name = 'task_details.html'
    success_url = reverse_lazy('task_list')

    def post(self, request, pk):
        
        task = get_object_or_404(Task, pk=pk)
        task.completed = True
        task.status = "Completa"
        task.save()
        
        return render(request, self.template_name, {'task': task})
        