#!/usr/bin/env python3
"""Module containing job application data form."""
from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    """
    Form for creating and updating job applications.

    This form is based on the JobApplication model. It-
    -includes fields for uploading a CV and providing a-
    -job description.

    Attributes:
        Meta: form config options that link it to JobApplication model.
    """
    class Meta:
        """
        Defines the model & fields for JobApplicationForm.
        """
        model = JobApplication
        fields = ['uploaded_file', 'job_description']
