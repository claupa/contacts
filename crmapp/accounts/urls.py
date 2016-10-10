from django.conf.urls import patterns, url
from crmapp.accounts.views import account_detail


account_urls =[url(r'^$', account_detail , name='account_detail'),]