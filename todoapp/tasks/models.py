from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    pass

class Tasks(models.Model):
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Completada', 'Completada'),
    ]
    TAGS_CHOICES = [
        ('Trabajo', 'Trabajo'),
        ('Hogar', 'Hogar'),
        ('Estudio', 'Estudio'),
        ('Otro', 'Otro'),
    ]
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES)
    tag = models.CharField(choices=TAGS_CHOICES)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title