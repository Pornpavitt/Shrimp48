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
    pond_name = models.TextField(max_length=255, null=True)
    pond_totalDays = models.IntegerField(null=True)
    pond_address = models.TextField(max_length=255,null=True)
    pond_number = models.IntegerField(null=True)
    pond_image = models.ImageField(upload_to='shrimp_ponds_images', blank=True, null=True)


class ShrimpPondsDetail(BaseModel):
    pond = models.ForeignKey(ShrimpPonds, on_delete=models.CASCADE)
    shrimp_quantity = models.IntegerField()
    shrimp_weight = models.FloatField()
    pond_dissolvedOxygen = models.FloatField()
    pond_waterHardness = models.FloatField()
    pond_pH = models.FloatField()
    pond_temperature = models.FloatField()
    food_quantity = models.FloatField()
    growth_rate = models.FloatField(null=True)
    predicted_growth_rate= models.FloatField(null=True)
    predicted_growth_rate_date_base = models.FloatField(null=True)
    predicted_growth_rate_weight_base = models.FloatField(null=True)
    survival_rate = models.FloatField()
    transparency = models.FloatField(null=True)
    salinity = models.FloatField(null=True)
    alkalinity = models.FloatField(null=True)
    nitrite = models.FloatField(null=True)
    TAN = models.FloatField(null=True)
    total_date = models.IntegerField()

class ShrimpFoods(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.TextField(max_length=255)
    food_description = models.TextField(max_length=255)
    allow_show = models.BooleanField(null=True)
    food_image = models.ImageField(upload_to='shrimp_foods_images', blank=True, null=True)


class ShrimpSpecies(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=255)
    specie_food = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    allow_show = models.BooleanField(null=True)
    image = models.ImageField(upload_to='shrimp_species_images', blank=True, null=True)


class ShrimpDiseases(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disease_name = models.TextField(max_length=255)
    disease_symptom = models.TextField(max_length=255)
    disease_cause = models.TextField(max_length=255)
    disease_prevent = models.TextField(max_length=255)
    disease_treat = models.TextField(max_length=255)
    allow_show = models.BooleanField(null=True)
    disease_image = models.ImageField(upload_to='shrimp_diseases_images', blank=True, null=True)

class ShrimpPrices(BaseModel):
    price_specie = models.TextField(max_length=255, null = True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    date = models.DateTimeField(null=True)
    predict=models.DecimalField(max_digits=10, decimal_places=2,null=True)

class Information(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    information_name = models.TextField(max_length=255)
    information_description = models.TextField(max_length=255)
    allow_show = models.BooleanField(null=True)
    information_image = models.ImageField(upload_to='shrimp_species_images', blank=True, null=True)