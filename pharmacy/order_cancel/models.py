from django.db import models

# Create your models here.
class signup_data(models.Model):
    email = models.CharField(max_length=122)
    pharmacy_name = models.CharField(max_length=122)
    password = models.CharField(max_length=128)

    
    def __str__(self):
        return self.name