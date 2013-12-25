from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'open_news.views.home', name='home'),
    # url(r'^open_news/', include('open_news.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
	url(r'^main/', include('main.urls')),
    url(r'^admin/', include(admin.site.urls)),
	
)
