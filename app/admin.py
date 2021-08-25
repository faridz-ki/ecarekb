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
            path('upload_portion', self.admin_view(admin_views.upload_portion), name='upload_portion'),
            path('upload_seasonality', self.admin_view(admin_views.upload_seasonality), name='upload_seasonality')
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

class AlternateNameAdmin(CustomModelAdmin):
    search_fields = ('food_name', 'alternate_name')

class FoodonIdAdmin(CustomModelAdmin):
    search_fields = ('food_name', 'foodon_id')

class ReferenceDataAdmin(CustomModelAdmin):
    search_fields = ['food_name']

class SeasonalityDataAdmin(CustomModelAdmin):
    search_fields = ['food_name']

custom_admin.register(MasterData, MasterDataAdmin)
custom_admin.register(PortionData, PortionDataAdmin)
custom_admin.register(AlternateName, AlternateNameAdmin)
custom_admin.register(FoodonId, FoodonIdAdmin)
custom_admin.register(ReferenceData, ReferenceDataAdmin)
custom_admin.register(SeasonalityData, SeasonalityDataAdmin)