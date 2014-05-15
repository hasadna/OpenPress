from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from open_news import views

admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^$',TemplateView.as_view(template_name='index.html'),),
                       url(r'*.css^$',TemplateView.as_view(template_name='index.html'),),
                       url(r'index.html\?.*^$', views.get_search, name='search',),
                       #url(r'timeline.html^$', views.get_search, name='search',),
                       url(r'^main/', include('main.urls')),
                       url(r'^admin/', include(admin.site.urls)),

)
