from django.contrib import admin
from .models import Usuario, Task, Tag, Comment, Priority

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Priority)