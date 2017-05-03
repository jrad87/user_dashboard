from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_id>\d+)$', views.show_user, name = 'show_user'),
    url(r'^(?P<user_id>\d+)/post_message$', views.post_message, name = 'post_message'),
    url(r'^(?P<user_id>\d+)/delete/(?P<message_id>\d+)$', views.delete_message, name = 'delete_message'),
    url(r'^(?P<message_id>\d+)/(?P<user_id>\d+)/post_comment$', views.post_comment, name = 'post_comment'),
    url(r'^(?P<user_id>\d+)/delete_comment/(?P<comment_id>\d+)$', views.delete_comment, name = 'delete_comment')
]
