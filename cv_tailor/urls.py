#!/usr/bin/env python3
"""Module to route data upload to upload view for processing."""
from django.urls import path
from .views import upload_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('upload/', upload_view, name='upload_view'),
]
