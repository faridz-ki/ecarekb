from rest_framework import serializers
from .models import MasterData, PortionData, AlternateName, FoodonId, ReferenceData, SeasonalityData

class MasterDataSerializer(serializers.Serializer):
    class Meta:
        model = MasterData
        fields = ('id', 'ghg', 'food_name', 'category', 'best_match', 'best_match_id', 'density')

class PortionDataSerializer(serializers.Serializer):
    class Meta:
        model = PortionData
        fields = ('id', 'food_id', 'food_name', 'food_unit', 'mass')

class AlternateNameSerializer(serializers.Serializer):
    class Meta:
        model = AlternateName
        fields = ('id', 'food_id', 'food_name', 'alternate_name')

class FoodonIdSerializer(serializers.Serializer):
    food_name = serializers.CharField(required=True, max_length=100)
    foodon_id = serializers.CharField(required=True,max_length=100)

    class Meta:
        model = FoodonId
        fields = ('id', 'food_id', 'food_name', 'foodon_id')

class ReferenceDataSerializer(serializers.Serializer):
    class Meta:
        model = ReferenceData
        fields = ('id', 'food_id', 'food_name', 'ghg', 'land_use', 'water_use')

class SeasonalityDataSerializer(serializers.Serializer):
    class Meta:
        model = SeasonalityData
        fields = ('id', 'food_id', 'food_name', 'month', 'land_use_change', 'feed', 'farm', 'processing', 'transport', 'packaging', 'retail')