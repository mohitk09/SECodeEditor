from django.conf.urls import url, include
from . import views
from material.frontend import urls as frontend_urls

urlpatterns = [
    url(r'^student/(?P<pk>\d+)/index.html$', views.index_student, name="index_student"),
    url(r'^faculty/(?P<pk>\d+)/index.html$', views.index_faculty, name="index_faculty"),
    url(r'^faculty/add_problem/index.html$', views.add_problem, name="index_problem"),
    url(r'^forgot_password/index.html$', views.forgot_password, name="forgot"),
    url(r'^login/index.html$', views.login, name="index_login"),
    url(r'', include(frontend_urls)),
]
