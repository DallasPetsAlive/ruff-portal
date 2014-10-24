from django.db import models

class Animal(models.Model):
    rg_id = models.IntegerField(unique=True, null=True)

