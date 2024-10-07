#!/usr/bin/env python3
"""Module to store uploaded file & job description."""
from django.db import models


class JobApplication(models.Model):
    """
    A model to represent a job application, comprised of-
    -an uploaded CV & a job description.

    Attributes:
        uploaded_file (FileField): user-uploaded CV.
        job_description (TextField): user-provided job description.
    """
    uploaded_file = models.FileField(upload_to='uploads/')
    job_description = models.TextField()

    def __str__(self) -> str:
        """
        Customization of default string method.

        Returns:
            str: the job description.
        """
        return self.job_description
