from django.conf.urls import url
from django.contrib import admin
from . import views
from django.urls import include


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.button),
    url(r'^zespol$', views.zespol),
    url(r'^external', views.external),
    url(r'^home1$', views.home1),
    url(r'^tinymce/', include('tinymce.urls')),
]