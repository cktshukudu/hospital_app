from django.urls import path
from . import views

urlpatterns = [
     path('index', views.index),
     path('admin1', views.admin1),
     path('', views.login),
     path('signup', views.signup),
     path('ratings', views.ratings),
     path('doctor_view', views.doctor_view),
     path('dashboards', views.dashboards),
     path('feedback', views.feedback),
     path('emp', views.create_emp),
     path('employees', views.view_emp),
     path('dep', views.create_dep),
     path('get/dep/all', views.view_dep),
     path('patient', views.create_patient),
     path('appointment', views.create_appointment),
     path('delete', views.delete_appointment),
     path('doctors_list', views.doctors_list),
     path('<int:link>/details', views.details),
     path('<int:id>/delete', views.delete_user),
     path('privilege/<str:name>', views.add_privilege),
     path('view_appointment', views.view_appointment)
]