from django.urls import path
from . import views

urlpatterns = [
     path('index', views.index),
     path('admin1', views.admin1),
     path('', views.login),
     path('signup', views.signup),
     path('ratings', views.ratings),
     path('dashboards', views.dashboards),
     path('feedback', views.feedback),
     path('create/emp', views.create_emp),
     path('get/emp/all', views.view_emp),
     path('create/dep', views.create_dep),
     path('get/dep/all', views.view_dep),
     path('create/patient', views.create_patient),
     path('create/appointment', views.create_appointment),
     path('delete', views.delete_appointment),
     path('doctors_list', views.doctors_list),
     path('<int:link>/details', views.details)
]