from django.contrib import admin
from .models import Usuario, Task, Tag

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Task)
admin.site.register(Tag)