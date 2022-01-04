from django.conf.urls import url, include
from rest_framework import routers
from .views import CodeViewSet,ResultViewSet,ResultCodeViewSet,CodeTestAPI
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

code_router = routers.DefaultRouter()
code_router.register(r"code", CodeViewSet)
#APIViewのCodeTestAPIをここに入れたい


result_router = routers.DefaultRouter()
result_router.register(r"result", ResultViewSet)

result_router.register(r"resultcode", ResultCodeViewSet)

#result_router.register(r"codetest", CodeTestAPI.as_view())
#追加部分
test_router = routers.SimpleRouter()

urlpatterns = [
  path('codetest', CodeTestAPI.as_view(), name='codetest'),
  #path('', include(test_router.urls)),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
