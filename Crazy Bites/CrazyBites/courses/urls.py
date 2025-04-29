from django.urls import path
from . import views

app_name = 'courses'  # Define the app namespace

urlpatterns = [
    path('italian/', views.italian_videos, name='italian_videos'),
    path('baking/', views.baking_videos, name='baking_videos'),
    path('asian/', views.asian_videos, name='asian_videos'),
    path('generate-certificate/', views.generate_certificate, name='generate_certificate'),
    path('download-certificate/', views.download_certificate, name='download_certificate'),
    path('enroll/', views.enroll_view, name='enroll'),
    path('process-enrollment/', views.process_enrollment, name='process_enrollment'),
] 