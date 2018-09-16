"""backend URL Configuration

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
from django.conf.urls import url, include
from rest_framework.authtoken import views as drf_views
from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from django.urls import path

from backend import views

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^api/$', views.api_root),
    url(r'^api/', include('soops.urls', namespace='soops')),

    url(r'^api/auth/', drf_views.obtain_auth_token, name='auth'),
    url(r'^api/docs/', include_docs_urls(
        title='Soop API', description='RESTful API for Soop')),

]
