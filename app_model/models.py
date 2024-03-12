from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import datetime
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timeNow}{old_filename}"
    return os.path.join('uploads/', filename)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True



class ShrimpPonds(BaseModel):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    pond_number = models.IntegerField()

class ShrimpPondsDetail(BaseModel):
    pondID = models.ForeignKey(ShrimpPonds, on_delete=models.CASCADE)
    shrimp_Quantity = models.IntegerField()
    Shrimp_Weight = models.IntegerField()
    pond_DissolvedOxygen = models.FloatField(max_length=100)
    pond_WaterHardness = models.FloatField(max_length=100)
    pond_pH = models.FloatField(max_length=100)
    pond_Temperature = models.FloatField(max_length=100)
    pond_TotalDays = models.IntegerField()
    food_Quantity = models.FloatField(max_length=100)
    growth_Rate = models.FloatField(max_length=100)
    survival_Rate = models.FloatField(max_length=100)
    total_Date = models.IntegerField()

class ShrimpFoods(BaseModel):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    food_Name = models.TextField(max_length=255)
    food_description = models.TextField(max_length=255)
    food_image = models.ImageField(upload_to='shrimp_foods_images', blank=True, null=True)


class ShrimpSpecies(BaseModel):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    FoodID = models.ForeignKey(ShrimpFoods, on_delete=models.CASCADE)
    name = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='shrimp_species_images', blank=True, null=True)


class ShrimpDiseases(BaseModel):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    disease_Name = models.TextField(max_length=255)
    disease_Symptom = models.TextField(max_length=255)
    disease_Cause = models.TextField(max_length=255)
    disease_Prevent = models.TextField(max_length=255)
    disease_Treat = models.TextField(max_length=255)
    disease_Image = models.ImageField(upload_to='shrimp_diseases_images', blank=True, null=True)

class ShrimpPrices(BaseModel):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    ShrimpSpeciesID = models.ForeignKey(ShrimpSpecies, on_delete=models.CASCADE)
    price = models.IntegerField()
