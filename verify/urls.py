from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.pictures_list),
    url(r'^uploads/', views.upload_file, name="uploads"),
    url(r'^login/', views.login, name="login"),
    url(r'^error/', views.error, name="error"),
    url(r'^success/', views.success, name="login_success"),
    url(r'^failed/', views.failed, name="login_failed"),
]