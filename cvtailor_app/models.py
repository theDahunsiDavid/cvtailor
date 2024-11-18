from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class JobApplication(models.Model):
    """Model for the user's CV and Job description upload."""
    uploaded_file = models.FileField(upload_to='uploads/')
    job_description = models.TextField()

    def __str__(self):
        return self.job_description[:50]


class User(AbstractUser):
    """
    The model for users of the CV Tailor platform.

    It makes Django's built user model for user auth,
    the User class, to inherit from AbstractUser class,
    enabling our HTML forms to use Django's built-in user auth.
    """
    def __str__(self):
        """Returns a str representation of the user."""
        return self.username
