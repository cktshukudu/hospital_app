from django.contrib import admin
from .models import Department, Doctor, Employees, Patients, Appointment, Rooms, Files

admin.site.register(Doctor)
admin.site.register(Department)
admin.site.register(Employees)
admin.site.register(Patients)
admin.site.register(Appointment)
admin.site.register(Rooms)
admin.site.register(Files)