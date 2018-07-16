"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from tastypie.api import Api
from bowling.api.resources import PlayerResource, FrameResource, ChanceResource, GameResource, PlayerGameResource, GamePlayerResource, GameManagerResource, UserResource


v1_api = Api(api_name='v1')
v1_api.register(PlayerResource())
v1_api.register(FrameResource())
v1_api.register(ChanceResource())
v1_api.register(GameResource())
v1_api.register(PlayerGameResource())
v1_api.register(GamePlayerResource())
v1_api.register(GameManagerResource())
v1_api.register(UserResource())

urlpatterns = [
    path('bowling/', include('bowling.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(v1_api.urls)),
]
