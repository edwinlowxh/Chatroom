from django.db import models

# Create your models here.
class groups(models.Model):
    group_name = models.CharField(max_length = 50)

class group_members(models.Model):
    username = models.CharField(max_length = 50)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    
