"""crmapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from marketing.views import HomePage
from crmapp.suscribers.views import subscriber_new
import django.contrib.auth.views as djauth
from crmapp.accounts.views import AccountList, account_cru
from accounts.urls import account_urls

urlpatterns = [
    # Marketing pages
    url(r'^$', HomePage.as_view(), name="home"),

    # Subscriber related URLs
    url(r'^signup/$', subscriber_new, name='sub_new'),

    # Admin URL
    url(r'^admin/', admin.site.urls),

    # Login/Logout URLs
    url(r'^login/$', djauth.login, {'template_name': 'login.html'}),
    url(r'^logout/$',djauth.logout, {'next_page': '/login/'}),

    # Account related URLs
    url(r'^account/list/$',AccountList.as_view(), name='account_list'),
    url(r'^account/(?P<uuid>[\w-]+)/', include(account_urls)),
    url(r'^account/new/$', account_cru, name='account_new'),
    # Contact related URLS
    
    # Communication related URLs
]
