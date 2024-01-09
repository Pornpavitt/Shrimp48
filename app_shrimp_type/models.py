from django.db import models
import datetime
import os
# Create your models here.
	# 4.shrimp species
	# 	-specie_ID
	# 	-specie_Name
	# 	-specie_Food
	# 	-specie_description
	# 	-user_ID(FK)
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = "%s%s", (timeNow,old_filename)
    return os.path.join('uploads/',filename)

class ShrimpSpecies(models.Model):
    name = models.TextField(max_length=255)
    food = models.TextField(max_length=255)
    description = models.TextField(max_length=255)
    
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self) -> str:
        return self.name
    
    def delete(self, *args, **kwargs):
        self.delete_at = datetime.datetime.now()
        self.save()

    def hard_delete(self, *args, **kwargs):
        super(ShrimpSpecies, self).delete(*args, **kwargs)

