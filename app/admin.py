from django.contrib import admin

# Register your models here.
from .models import MasterData, PortionData, AlternateName, FoodonId, ReferenceData, SeasonalityData

admin.site.register(MasterData)
admin.site.register(PortionData)
admin.site.register(AlternateName)
admin.site.register(FoodonId)
admin.site.register(ReferenceData)
admin.site.register(SeasonalityData)