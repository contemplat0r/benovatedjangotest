from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from accounts.views import transfer
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'benovatetest.views.home', name='home'),

    #url(r'^$', TemplateView.as_view(template_name='accounts/transfer.html'), name='transfer'),
    url(r'^$', transfer, name='transfer'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}))
