from django.urls import path
from django.conf.urls import url, include

from django.contrib.auth import views as auth_views
from komikrepo import views as komik_views
from . import views

app_name = 'komikrepo'

urlpatterns = [
    path('', views.index, name='index'),


    url( r'^login/$',auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    url(r'^signup/$', komik_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    url(r'^account/(?P<username>[\w.@+-]+)/$', komik_views.accountView, name='account'),
    url(r'^account/delete/(?P<username>[\w.@+-]+)/$', komik_views.deleteAccount, name='deleteAccount'),
    url(r'^account/edit/(?P<username>[\w.@+-]+)/$', komik_views.editAccount, name='editAccount'),

    url(r'^komiks/$',  komik_views.listKomiks, name='listKomiks'),
    path('komiks/<int:page>/', komik_views.listKomiks, name='listKomiks'),
    path('komik/<int:id>/', komik_views.viewKomik, name='viewKomik'),

    path('review/<int:id>/', komik_views.reviewKomik, name='reviewKomik'),
    path('review/edit/<int:id>/', komik_views.editReviewKomik, name='editReviewKomik'),
    path('review/elete/<int:id>/', komik_views.deleteReviewKomik, name='deleteReviewKomik'),


]
