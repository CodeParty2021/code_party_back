from django.urls import path
from .views import FirebaseAuthView, UserRetrieveView


urlpatterns = [
    path("auth/", FirebaseAuthView.as_view()),
    path("<pk>/", UserRetrieveView.as_view()),
]
