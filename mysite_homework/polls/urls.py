from django.conf.urls import url
from . import views


app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^$', views.index, name='return_mainpage'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^question/', views.add_question, name='add_question'),
    url(r'^(?P<question_id>[0-9]+)/add_choice/$', views.add_choice, name='add_choice'),
    url(r'^delete_question/$', views.choice_delete_question, name='delete_q'),
]
