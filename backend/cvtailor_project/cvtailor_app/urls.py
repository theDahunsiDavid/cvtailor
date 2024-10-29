from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import convert_to_ats_format

urlpatterns = [
    path('', views.home, name="home"),
    path('upload/', views.upload_cv, name="upload_cv"),
    path('convert_ats/', convert_to_ats_format, name='convert_ats'),
    # path('apply_suggestion/', views.apply_suggestion, name='apply_suggestion'),
    # path('download_docx/', views.download_docx, name='download_docx'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
