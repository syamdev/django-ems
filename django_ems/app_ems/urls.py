from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^employees/profile/list/$', views.ProfileListView.as_view(), name='profile_list'),
    re_path(r'^employees/(?P<pk>[0-9]+)/profile/$', views.ProfileDetailView.as_view(), name='profile_detail'),
    re_path(r'^employees/profile/create/$', views.ProfileCreateView.as_view(), name='profile_create'),
    re_path(r'^employees/(?P<pk>[0-9]+)/profile/update/$', views.ProfileUpdateView.as_view(), name='profile_update'),
    re_path(r'^employees/(?P<pk>[0-9]+)/profile/delete/$', views.ProfileDeleteView.as_view(), name='profile_delete'),
]