from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'webapp'

urlpatterns = [
    path('', views.upload_files, name = 'upload_files'),
    path('jobs/<uuid:pk>', views.job_results, name = 'job_results'),
    path('download/<uuid:pk>/<str:filename>', views.download, name = 'download'),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )
