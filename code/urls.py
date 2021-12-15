from rest_framework import routers
from .views import CodeViewSet,ResultViewSet,ResultCodeViewSet,CodeTestAPI


code_router = routers.DefaultRouter()
code_router.register(r"code", CodeViewSet)
#APIViewのCodeTestAPIをここに入れたい

result_router = routers.DefaultRouter()
result_router.register(r"result", ResultViewSet)

result_router.register(r"resultcode", ResultCodeViewSet)
