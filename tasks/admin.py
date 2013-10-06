from django.contrib import admin
from tasks import models
from django.contrib.admin.options import ModelAdmin

class TaskAdmin(ModelAdmin):
    list_display = ('description', 'frequency')

admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Supplier)
admin.site.register(models.Estimate)