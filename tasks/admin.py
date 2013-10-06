from django.contrib import admin
from tasks import models
from django.contrib.admin.options import ModelAdmin

class TaskAdmin(ModelAdmin):
    list_display = ('description', 'frequency')
    
class SupplierAdmin(ModelAdmin):
    list_display = ('name', 'website', 'telephone')

admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Supplier, SupplierAdmin)
admin.site.register(models.Contact)
admin.site.register(models.Estimate)