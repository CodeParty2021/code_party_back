from rest_framework import routers
from .views import FirebaseAuthView


router = routers.DefaultRouter()
router.register(r"auth", FirebaseAuthView.as_view())

urlpatterns
