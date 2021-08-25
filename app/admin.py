from django.contrib import admin

from . import admin_views
from django.urls import path
# Register your models here.
from .models import MasterData, PortionData, AlternateName, FoodonId, ReferenceData, SeasonalityData


class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload', self.admin_view(admin_views.upload), name='upload'),
            path('upload_foodon', self.admin_view(admin_views.upload_foodon), name='upload_foodon'),
            path('upload_portion', self.admin_view(admin_views.upload_portion), name='upload_portion')
        ]
        return custom_urls + urls
        
custom_admin = MyAdminSite()

class CustomModelAdmin(admin.ModelAdmin):
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.list_editable = [field.name for field in model._meta.fields if field.editable and field.name != "id"]
        self.list_display_links = None
        super(CustomModelAdmin, self).__init__(model, custom_admin)

class MasterDataAdmin(CustomModelAdmin):
    search_fields = ('food_name', 'category', 'best_match')

class PortionDataAdmin(CustomModelAdmin):
    search_fields = ('food_name', 'portion')


custom_admin.register(MasterData, MasterDataAdmin)
custom_admin.register(PortionData, PortionDataAdmin)
custom_admin.register(AlternateName)
custom_admin.register(FoodonId)
custom_admin.register(ReferenceData)
custom_admin.register(SeasonalityData)