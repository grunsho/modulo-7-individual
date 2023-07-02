from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Completada', 'Completada'),
    ]
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, blank=False)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, blank=False)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title