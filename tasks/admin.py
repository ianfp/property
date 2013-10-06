from django.contrib import admin
from tasks import models
from django.contrib.admin.options import ModelAdmin

class TaskAdmin(ModelAdmin):
    list_display = ('description', 'frequency')
    
class SupplierAdmin(ModelAdmin):
    list_display = ('name', 'website', 'telephone')
    filter_horizontal = ('contacts', )
    
class ContactAdmin(ModelAdmin):
    list_display = ('__str__', 'email', 'telephone')
    
class EstimateAdmin(ModelAdmin):
    filter_horizontal = ('tasks', )

admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Supplier, SupplierAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Estimate, EstimateAdmin)