"""code_party_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from code.models import Code

from testapp.urls import router as testmodel_router
from code.urls import code_router ,result_router


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(testmodel_router.urls)),
    #path("code/",include(code_router.urls)),
    path("result/",include(result_router.urls)),
    path("code/",include('code.urls'))
]
