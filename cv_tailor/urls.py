#!/usr/bin/env python3
"""Module to route data upload to upload view for processing."""
from django.urls import path
from .views import upload_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_view, name='upload_view'),
]
