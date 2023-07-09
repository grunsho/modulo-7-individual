from django.contrib.auth.forms import forms
from django import forms
from .models import Usuario, Task, Comment

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, label='Nombre de Usuario', error_messages={
        'required': 'El nombre de usuario es obligatorio'})
    password = forms.CharField(max_length=16, required=True, label='Contraseña',
        widget=forms.PasswordInput, error_messages={'required': 'La contraseña es obligatoria'})
    class Meta:
        model = Usuario

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['tag'].empty_label = 'Filtrar tareas por etiqueta'
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'tag', 'completed']
        labels = {
            'title': 'Título de la tarea',
            'description': 'Descripción',
            'due_date': 'Fecha de vencimiento',
            'status': 'Estado de la tarea',
            'tag': 'Etiqueta',
            'completed': 'Completa'
        }
        widgets = {
            'title': forms.TextInput(attrs= {'class': 'form-control'}),
            'description': forms.Textarea(attrs= {'class':'form-control'}),
            'due_date': forms.DateInput(format=('%Y-%m-%d'), attrs= {'class':'form-control', 'placeholder': 'Fecha', 'type': 'date'}),
            'status': forms.Select(attrs= {'class':'form-control'}),
            'tag': forms.Select(attrs= {'class':'form-control'}),
            'completed': forms.CheckboxInput()
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
        labels = { 'text':'Nuevo comentario:'}
        widgets = { 'text': forms.Textarea(attrs={'class':'form-control'})}