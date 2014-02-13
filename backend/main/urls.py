from django.conf.urls import patterns, url
from django.contrib import admin
from main import views
from models import Archive, Title, Volume, Section, Page, Article, Paragraph


urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index',),
                       url(r'^search/$', views.SearchResultsView.as_view(), name='search'),
                       url(r'article/(?P<pk>[0-9]+)/$', views.ResultDetailView.as_view(), name='article-detail')
)
