#!/usr/bin/env python3
"""Module to route data upload to upload view for processing."""
from django.urls import path
from .views import index, upload_view

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_view, name='upload_view'),
]
