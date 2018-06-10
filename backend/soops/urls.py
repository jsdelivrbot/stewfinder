from django.conf.urls import url, include
from rest_framework.authtoken import views as drf_views
from rest_framework.documentation import include_docs_urls

from soops import views

# app_name must go here to specify the namespace
app_name='soops'

urlpatterns = [
    url(r'^soops/$', views.SoopList.as_view(), name='soop-list'),
    url(r'^soops/(?P<pk>[0-9]+)/$', views.SoopDetail.as_view(),
        name='soop-detail'),
]
