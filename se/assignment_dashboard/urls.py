from django.conf.urls import url, include
from . import views
from material.frontend import urls as frontend_urls

urlpatterns = [
    url(r'^student/index.html$', views.index_student, name="index_student"),
    url(r'^faculty/index.html$', views.index_faculty, name="index_faculty"),
    url(r'^faculty/add_problem/index.html$', views.add_problem, name="index_problem"),
    url(r'^faculty/problems/index.html$', views.problems, name="index_problem_f"),
    url(r'^login/index.html$', views.index_login, name="index_login"),
    url(r'^logout.html$', views.index_logout, name="index_logout"),
    url(r'', include(frontend_urls)),
]
