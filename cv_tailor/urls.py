#!/usr/bin/env python3
"""Module to route data upload to upload view for processing."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_view, name='upload_view'),
]
