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


#追加部分
urlpatterns = [
  path('test', CodeTestAPI.as_view(), name='codetest'),
  path('', include(code_router.urls)),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
