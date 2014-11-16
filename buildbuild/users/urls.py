from django.conf.urls import patterns, include, url
from users import views

from users.views import UsersIndexView, UserShowView 
from users.views import Login, Logout, SignUp, AccountView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url('^$', UsersIndexView.as_view(), name = "index"),
    url('^(?P<pk>\d+)$', UserShowView.as_view(), name = "show"),
    url(r'^account/', login_required(AccountView.as_view()), name="account"),
    url(r'^([0-9]+)/$', 'users.views.user_page', name="user_page"), 
)

