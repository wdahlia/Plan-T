from django.contrib import admin
from .models import Todos

# Register your models here.
class TodosAdmin(admin.ModelAdmin):
    pass


admin.site.register(Todos, TodosAdmin)