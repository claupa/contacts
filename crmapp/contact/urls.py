from django.conf.urls import patterns, url
from .views import contact_detail, contact_cru

contact_urls =[
    url(r'^contact/new/$',contact_cru, name='contact_new'),
    url(r'^$', contact_detail, name="contact_detail"),

]