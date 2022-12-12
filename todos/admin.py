from django.contrib import admin

# Register your models here.
class TodosAdmin(admin.ModelAdmin):
    pass


admin.site.register(Todos, TodosAdmin)