from django.conf.urls import patterns, url
from tasks import views

urlpatterns = patterns('',
    url(r'^upload/', views.upload, name="upload"),
    url(r'^report/', views.report, name="report"),
)