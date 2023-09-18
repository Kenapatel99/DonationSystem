from django.urls import re_path

from . import views

# router = routers.DefaultRouter()
# router.register(r'user_data', views.UserData)

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^home/$', views.home, name='home'),
    re_path(r'^member/$', views.member, name='member'),
    re_path(r'^otp/$', views.otp_verification, name='otp'),
    # re_path(r'^$', views.home1, name='home'),
    re_path(r'^payment/$', views.payment, name='payment'),
    re_path(r'^response', views.response, name='response'),

]