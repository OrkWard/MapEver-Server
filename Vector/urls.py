from django.urls import path
from .views import overlay

app_name = "Vector"

urlpatterns = [
    path('overlay/', overlay)
]