from django.conf.urls import patterns, url
from .views import contact_detail

contact_urls =[

    url(r'^$', contact_detail, name="contact_detail"),

]