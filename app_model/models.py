from django.db import models , migrations
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True



class ShrimpPonds(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pond_name = models.TextField(max_length=255 , null = True)

class ShrimpPondsDetail(BaseModel):
    pond = models.ForeignKey(ShrimpPonds, on_delete=models.CASCADE)
    shrimp_quantity = models.IntegerField()
    shrimp_weight = models.IntegerField()
    pond_dissolvedOxygen = models.FloatField(max_length=100)
    pond_waterHardness = models.FloatField(max_length=100)
    pond_pH = models.FloatField(max_length=100)
    pond_temperature = models.FloatField(max_length=100)
    pond_totalDays = models.IntegerField()
    food_quantity = models.FloatField(max_length=100)
    growth_rate = models.FloatField(max_length=100)
    survival_rate = models.FloatField(max_length=100)
    total_date = models.IntegerField()

class ShrimpFoods(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.TextField(max_length=255)
    food_description = models.TextField(max_length=255)
    food_image = models.ImageField(upload_to='shrimp_foods_images', blank=True, null=True)


class ShrimpSpecies(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=255)
    specie_food = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='shrimp_species_images', blank=True, null=True)


class ShrimpDiseases(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease_name = models.TextField(max_length=255)
    disease_symptom = models.TextField(max_length=255)
    disease_cause = models.TextField(max_length=255)
    disease_prevent = models.TextField(max_length=255)
    disease_treat = models.TextField(max_length=255)
    disease_image = models.ImageField(upload_to='shrimp_diseases_images', blank=True, null=True)

class ShrimpPrices(BaseModel):
    price_specie = models.TextField(max_length=255, null = True)
    price = models.IntegerField()
