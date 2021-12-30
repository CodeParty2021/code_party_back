from django.urls import path
from rest_framework import routers
from .views import FirebaseAuthView


urlpatterns = [path("auth", FirebaseAuthView.as_view())]
