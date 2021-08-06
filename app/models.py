from django.db import models

class ReferenceData(models.Model):
    id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=20)
    ghg_global = models.FloatField()
    ghg_retail = models.FloatField()
    food_name = models.CharField(max_length=20)
    land_use = models.CharField(max_length=15, blank=True)
    water_use = models.CharField(max_length=15, blank=True)
    land_use_change = models.FloatField()
    feed = models.FloatField()
    farm = models.FloatField()
    processing = models.FloatField()
    transport = models.FloatField()
    packaging = models.FloatField()
    retail = models.FloatField()

    class Meta:
        ordering = ['food_name']
    
    def __str__(self):
        return self.food_name

class MasterData(models.Model):
    id = models.AutoField(primary_key=True)
    ghg_global = models.FloatField()
    ghg_retail = models.FloatField()
    food_name = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    best_match = models.CharField(max_length=20)
    best_match_id = models.ForeignKey(ReferenceData, on_delete=models.CASCADE)
    density = models.FloatField()

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.food_name

class PortionData(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=10, blank=True)
    food_id = models.ForeignKey(MasterData, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=20)
    # May need to change to using enumerated types for food units
    portion = models.CharField(max_length=20)
    weight = models.FloatField()

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.food_name

class AlternateName(models.Model):
    id = models.AutoField(primary_key=True)
    food_id = models.ForeignKey(MasterData, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=20)
    alternate_name = models.CharField(max_length=30)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.food_name

class FoodonId(models.Model):
    id = models.AutoField(primary_key=True)
    food_id = models.ForeignKey(MasterData, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=20)
    foodon_id = models.TextField(max_length=50)

    class Meta:
        ordering = ['food_id']
    
    def __str__(self):
        return self.food_name


class SeasonalityData(models.Model):
    id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=20)
    reference_id = models.ForeignKey(ReferenceData, on_delete=models.CASCADE)
    month = models.IntegerField()
    land_use_change = models.FloatField()
    feed = models.FloatField()
    farm = models.FloatField()
    processing = models.FloatField()
    transport = models.FloatField()
    packaging = models.FloatField()
    retail = models.FloatField()
    ghg = models.FloatField()
