from django.contrib import admin
from tasks import models
from django.contrib.admin.options import ModelAdmin

class AssetAdmin(ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ('location', )

class TaskAdmin(ModelAdmin):
    list_display = ('__str__', 'location', 'frequency', 'next_due')
    list_filter = ('asset__location', )
    
class SupplierAdmin(ModelAdmin):
    list_display = ('name', 'website', 'telephone')
    filter_horizontal = ('contacts', )
    
class ContactAdmin(ModelAdmin):
    list_display = ('__str__', 'email', 'telephone')
    
class QuoteAdmin(ModelAdmin):
    filter_horizontal = ('tasks', )

admin.site.register(models.Property)
admin.site.register(models.Location)
admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Supplier, SupplierAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Quote, QuoteAdmin)