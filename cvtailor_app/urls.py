from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import convert_to_ats_format
from .views import implement_suggestion

urlpatterns = [
    path('', views.home, name="home"),
    path('signUp', views.signUp, name='signUp'),
    path('signIn', views.signIn, name='signIn'),
    path('signOut', views.signOut, name='signOut'),
    path('upload/', views.upload_cv, name="upload_cv"),
    path('convert_ats/', convert_to_ats_format, name='convert_ats'),
    # path('download_docx/', views.download_docx, name='download_docx'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('api/implement_suggestion', implement_suggestion, name='implement_suggestion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
