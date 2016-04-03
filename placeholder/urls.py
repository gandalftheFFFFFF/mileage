from django.conf.urls import url, include
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='placeholder/milage-index.html')),
    url(r'^$', index, name='milage-index'),
    url(r'^cars/$', cars, name='cars'),
    url(r'^history/$', history, name='history'),
    url(r'^overview/$', overview, name='overview'),
    url(r'upload/$', upload_csv, name='upload'),
    url(r'^delete/([0-9]+)/$', delete, name='delete'),
    url(r'^edit/([0-9]+)/$', edit, name='edit'),
    url(r'^history/clear$', clear_history, name='clear_history')
]