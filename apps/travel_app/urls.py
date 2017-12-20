from django.conf.urls import url
from . import views
print "****************************app urls.py"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^register$', views.create, name = 'create'),
    url(r'^travels$', views.index, name = 'travels'),
    url(r'^plan_create$', views.plan_create, name = 'plan_create'),
    url(r'^new_plan$', views.new_plan, name = 'new_plan'),
    url(r'^home$', views.home, name = 'home'),
    url(r'^join/(?P<plan_id>\d+)$', views.join_plan, name = 'join'),
    url(r'^plan/(?P<plan_id>\d+)$', views.plan, name = "plan"),
]
