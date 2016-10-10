from django.conf.urls import patterns, url
from crmapp.accounts.views import account_detail, account_cru


account_urls =[url(r'^$', account_detail , name='account_detail'),
url(r'^edit/$',account_cru, name='account_update'
    ),]