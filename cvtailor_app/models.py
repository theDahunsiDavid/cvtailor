from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class JobApplication(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')
    job_description = models.TextField()

    def __str__(self):
        return self.job_description[:50]
