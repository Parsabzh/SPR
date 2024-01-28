from django.db import models

class component (models.Model):
    name= models.CharField(max_length=50)
    vesion= models.CharField(max_length=10)

