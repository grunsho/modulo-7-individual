from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name

class Priority(models.Model):
    priority = models.CharField(max_length=100, blank=False)
    
    def __str__(self):
        return self.priority

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Completa', 'Completa'),
    ]
    
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.ForeignKey(Priority, on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, blank=False)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, blank=False)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentario creado el {self.created_at}"