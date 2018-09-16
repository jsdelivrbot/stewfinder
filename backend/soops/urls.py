from django.conf.urls import include, url
from django.urls import path
from rest_framework.authtoken import views as drf_views
from rest_framework.documentation import include_docs_urls
from soops import views

# app_name must go here to specify the namespace
app_name = 'soops'

urlpatterns = [
    url(r'^soops/$', views.SoopList.as_view(), name='soop-list'),
    url(r'^soops/(?P<pk>[0-9]+)/$', views.SoopDetail.as_view(),
        name='soop-detail'),
    # url(r'^soops/(?P<pk>[0-9]+)/votes$', views.SoopVotes, name='soop-votes'),
    path('soops/<int:soop_id>/votes/number',
         views.GetNumVotes, name='all-votes'),
    path('soops/<int:soop_id>/votes/up', views.VoteUp, name='up-vote'),
    path('soops/<int:soop_id>/votes/down', views.VoteDown, name='down-vote'),
    path('soops/<int:soop_id>/votes/user', views.UserVotes, name='user-vote'),
    path('soops/<int:soop_id>/votes/delete', views.VoteDelete,
         name='delete-vote'),
]
