from django.db import models

# Create your models here.

class user_data(models.Model):
    name = models.CharField(max_length=122)
    user_name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    password = models.CharField(max_length=128)
    access_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
