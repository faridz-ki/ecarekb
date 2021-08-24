from django.contrib import admin

# Register your models here.
from .models import MasterData, PortionData, AlternateName, FoodonId, ReferenceData, SeasonalityData

class CustomModelAdmin(admin.ModelAdmin):
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        self.list_editable = [field.name for field in model._meta.fields if field.editable and field.name != "id"]
        self.list_display_links = None
        super(CustomModelAdmin, self).__init__(model, admin_site)

class MasterDataAdmin(CustomModelAdmin):
    search_fields = ('food_name', 'category', 'best_match')

class PortionDataAdmin(CustomModelAdmin):
    search_fields = ('food_name', 'portion')
admin.site.register(MasterData, MasterDataAdmin)
admin.site.register(PortionData, PortionDataAdmin)
admin.site.register(AlternateName)
admin.site.register(FoodonId)
admin.site.register(ReferenceData)
admin.site.register(SeasonalityData)