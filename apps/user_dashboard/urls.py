from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',                 views.index,            name = 'index'),
    url(r'^signin$',           views.signin,           name = 'signin'),
    url(r'^signin/process$',   views.signin_process,   name = 'signin_process'),
    url(r'^signout$',          views.signout,          name = 'signout'),
    url(r'^register$',         views.register,         name = 'register'),
    url(r'^register/process$', views.register_process, name = 'register_process'),
    url(r'^dashboard$',        views.dashboard,        name = 'dashboard'),
    url(r'^users$',            views.users,            name = 'users'),
    url(r'^users/new$',        views.new_user,         name = 'new_user'),
    url(r'^users/new/process$',  views.user_new_process, name = 'user_new_process'),
    url(r'^users/edit$',         views.edit_user,        name = 'edit_user'),
    url(r'^users/edit/(?P<user_id>\d+)$',                    views.admin_edit_user,          name = 'admin_edit_user'),
    url(r'^users/edit/(?P<user_id>\d+)/info/process$',       views.edit_info_process,        name = 'edit_info_process'),
    url(r'^users/edit/(?P<user_id>\d+)/password/process$',   views.edit_password_process,    name = 'edit_password_process'),
    url(r'^users/edit/(?P<user_id>\d+)/description/process$',views.edit_description_process, name = 'edit_description_process'),
    url(r'^users/(?P<user_id>\d+)/remove$',                  views.admin_remove_user,        name = 'admin_remove_user')
]
