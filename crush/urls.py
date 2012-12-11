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
    url(r'^preview/$', 'crush_connector.views.index'),
    url(r'^$', 'crush_connector.views.splash'),
    url(r'^auth/', 'crush_connector.views.auth'),
    url(r'^ctest/', 'ctest.views.index'),
    url(r'^about/', 'crush_connector.views.about'),
    url(r'^submit/', 'crush_connector.views.submit'),
    url(r'^success/', 'crush_connector.views.success'),
    url(r'^form/$', 'crush_connector.views.form'),
    url(r'^name-lookup/(.*)', 'name_lookup.views.lookup_mit_people'),
    url(r'^getlabels/', 'crush_connector.views.getlabels'),
    url(r'^clearmiddlenames/', 'crush_connector.views.clearMiddleNames'),
    url(r'^populate-names/', 'name_lookup.views.populate_names'),
    url(r'^names/', 'crush_connector.views.getnames'),
    url(r'^need_certificate/', 'crush_connector.views.need_certificate'),
    url(r'^over_limit/', 'crush_connector.views.over_limit'),

                       )
