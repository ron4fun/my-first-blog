from django.conf.urls import url
from . import views

urlpatterns = [    
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^$', views.home, name='home'),

    # previous login view
    #url(r'^login/$', views.user_login, name='login'),
    
    url(r'^register/$', views.register, name='register'),

    #url(r'^feedback/$', views.feedback, name='feedback'),
    #url(r'^recieve-cash/$', views.recieveCash, name='recieve_cash'),
    url(r'^transactions/$', views.transactions, name='transactions'),

    # login / logout urls
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^logout-then-login/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout_then_login'),

    # change password urls
    url(r'^password-change/$',
        'django.contrib.auth.views.password_change',
        {'post_change_redirect': '/password-change-done/',
         'template_name': 'registration/password_change_form.html'},
        name='password_change'),
    url(r'^password-change-done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),
    
    # restore password urls
    url(r'^password-reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/password-reset-done/',
         'template_name': 'registration/password_reset_form.html'},
        name='password_reset'),
    url(r'^password-reset-done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'registration/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/password-reset-complete/',
         'template_name': 'registration/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^password-reset-complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'registration/password_reset_complete.html'},
        name='password_reset_complete'),
    ]



