from django.contrib import admin
from .models import Todos

# Register your models here.
class TodosAdmin(admin.ModelAdmin):
    fields = ("user_id", "title", "content", "when", "started_at", "expired_at", "is_completed")


admin.site.register(Todos, TodosAdmin)