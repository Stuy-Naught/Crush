from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crush.views.home', name='home'),
    # url(r'^crush/', include('crush.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^connect/', 'crush_connector.views.register'),
    url(r'^ctest/', 'ctest.views.index'),
    url(r'^about/', 'crush_connector.views.about'),
    url(r'^validate/(.+)/(\d{10})/', 'crush_connector.views.validate'),
    url(r'^$', 'crush_connector.views.register'),
    url(r'^name-lookup/(.*)', 'name_lookup.views.lookup_mit_people'),
    url(r'^populate-names/', 'name_lookup.views.populate_names')
)
