#!/usr/bin/env python3
"""Module to manage my models w/ Django admin interface."""
from django.contrib import admin
from .models import JobApplication

admin.site.register(JobApplication)
