from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Doctor, Employees, Department, Patients, Appointment, Rating, UserPrivileges, AppovedUsers
from django.db.models import Avg
import datetime
from django.template import RequestContext
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate
from cryptography.fernet import Fernet

def ratings(request):
        employees = Employees.objects.all()
        patients = Patients.objects.all()
        ratings = Rating.objects.all()
        New_user = AppovedUsers.objects.get(authenticated=True)
        rate_star = 0
        if request.method == 'POST':
                doctors = Employees.objects.filter(Role='Doctor')
                worker = request.POST.get('employee')
                employee = Employees.objects.get(id=worker)
                client = request.POST.get('patient')
                patient = Patients.objects.get(id=client)
                feedback = request.POST.get('feedback')
                star = request.POST.get('value', 'Not Found')
                rate = Rating(Patient=patient, Employee=employee, Rate=star, Feedback=feedback)
                rate.save()
                rates = Rating.objects.filter(Employee=worker).aggregate(Avg('Rate'))
                ratesCount = Rating.objects.filter(Employee=worker).count()
                employer = Employees.objects.get(id=worker)
                employer.Rates = rates['Rate__avg']
                employer.NumOfRates = ratesCount
                employer.save()

                return render(request, 'hospital/admin1.html',{'ratings':ratings})
        return render(request, 'hospital/ratings.html', {'employees': employees, 'patients': patients, 'rate': rate_star, 'user': New_user})

def doctors_list(request):
       doctors = Employees.objects.filter(Role='Doctor')
       New_user = AppovedUsers.objects.get(authenticated=True)
       return render(request, 'hospital/doctor_list.html', {'doctors': doctors, 'user': New_user})

def login(request):
        if request.method == 'POST':
               username = request.POST.get('username')
               password = request.POST.get('password')
               try:
                     user = AppovedUsers.objects.get(username=username)
                     if password == user.password:
                            user.authenticated = True
                            user.last_login = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            user.save()
                            return render(request, 'hospital/dashboards.html')
                     else:
                            messages.error(request, 'Incorrect username/password')
                            return render(request, 'hospital/login.html')
               except AppovedUsers.DoesNotExist:
                      messages.error(request, 'Incorrect username/password')
                      return render(request, 'hospital/login.html')
        else:
                try:
                        New_user = AppovedUsers.objects.get(authenticated=True)
                        New_user.authenticated = False
                        New_user.save()
                except AppovedUsers.DoesNotExist:
                       pass
                return render(request, 'hospital/login.html')
def signup(request):
        privileges = UserPrivileges.objects.all()
        if request.method == 'POST':
               username = request.POST.get('username')
               email = request.POST.get('email')
               password = request.POST.get('password')
               cellnumber = request.POST.get('cellnumber')
               staff = request.POST.get('staff')
               privilege = request.POST.get('privilege')
               chosenPrivilege = UserPrivileges.objects.get(id=privilege)
               try:
                     staff_number = Employees.objects.get(Staff_number=staff)
                     new_user = AppovedUsers(username=username, EmailAddress=email, password=password, CellNumber=cellnumber, Employee=staff_number, UserPrivilege=chosenPrivilege, last_login=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                     new_user.save()
                     return render(request, 'hospital/login.html')
               except Employees.DoesNotExist:
                     messages.error(request, 'Invalid staff number')
                     return render(request, 'hospital/signup.html', {'privileges': privileges})
               except IntegrityError:
                     messages.error(request, 'Username, cellnumber or email already exists')
                     return render(request, 'hospital/signup.html', {'privileges': privileges})
               
        else:
                return render(request, 'hospital/signup.html', {'privileges': privileges})
        
def admin1(request):
        ratings = Rating.objects.all()
        New_user = AppovedUsers.objects.get(authenticated=True)
        return render(request, 'hospital/admin1.html',{'ratings':ratings, 'user': New_user})

def create_emp(request):
        departments = Department.objects.all()
        if request.method == 'POST':
                name = request.POST.get('names')
                l_name = request.POST.get('l_name')
                DOB = request.POST.get('DOB')
                staff = request.POST.get('staff_no')
                start = request.POST.get('start_date')
                role = request.POST.get('role')
                specialization = request.POST.get('Specialization')
                department = request.POST.get('department')
                dep = Department.objects.get(id=department)
                employee = Employees(Fnames=name, Lname=l_name, DOB=DOB, Staff_number=staff, start_date=start, Role=role, Specialization=specialization, Department=dep)
                employee.save()
                messages.success(request, 'Employee  Successfully Added')
                return render(request, 'hospital/create_emp.html', {'departments': departments})
        else:
                New_user = AppovedUsers.objects.get(authenticated=True)
                return render(request, 'hospital/create_emp.html', {'departments': departments, 'user': New_user})
        
def details(request, link):
       doctor = Employees.objects.get(id=link)
       New_user = AppovedUsers.objects.get(authenticated=True)
       return render(request, 'hospital/doctor-details.html', {'doctor': doctor, 'user': New_user})

def view_emp(request):
       employees = Employees.objects.all()
       New_user = AppovedUsers.objects.get(authenticated=True)
       return render(request, 'hospital/view_emp.html', {'employees': employees, 'user': New_user})

def create_dep(request):
        if request.method == 'POST':
                name = request.POST.get('dep_name')
                description = request.POST.get('description')
                phone = request.POST.get('cellphone')
                email = request.POST.get('email')
                location = request.POST.get('location')
                department = Department(Dep_Name= name, Description=description, Phone=phone, Email=email, Location=location, Date_Added= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), Date_Update=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                department.save()
                return render(request, 'hospital/dashboards.html')
        else:
                New_user = AppovedUsers.objects.get(authenticated=True)
                return render(request, 'hospital/create_dep.html', {'user': New_user})

def view_dep(request):
       departments = Department.objects.all()
       New_user = AppovedUsers.objects.get(authenticated=True)
       return render(request, 'hospital/view_dep.html', {'departments': departments, 'user': New_user})

def create_patient(request):
       if request.method == 'POST':
              names = request.POST.get('Fnames')
              lname = request.POST.get('Lname')
              gender = request.POST.get('gender')
              DOB = request.POST.get('DOB')
              address = request.POST.get('Address')
              phone = request.POST.get('Phn_no')
              email = request.POST.get('Email')
              patient = Patients(F_names=names, L_name=lname, Gender=gender, DOB=DOB, Address=address, Phn_no=phone, Email=email, Date_Added=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), Date_Updated=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
              patient.save()
              messages.success(request, 'Patient Succesfully Added.')
              return render(request, 'hospital/create_patient.html')
       else:
              New_user = AppovedUsers.objects.get(authenticated=True)
              return render(request, 'hospital/create_patient.html', {'user': New_user})
       
def create_appointment(request):
       if request.method == 'POST':
              patient = request.POST.get('patient')
              pat_data = Patients.objects.get(id=patient)
              doctor = request.POST.get('doctor')
              doc_data = Employees.objects.get(id=doctor)
              description = request.POST.get('description')
              app_date = request.POST.get('app_date')
              appointment = Appointment(Patient=pat_data, Doctor=doc_data, Description=description, Date_set=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), App_date=app_date, Date_updated=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
              appointment.save()
              return render(request, 'hospital/create_appointment.html', {'patients': patients, 'doctors': doctors})
       else:
              patients = Patients.objects.all()
              doctors = Employees.objects.filter(Role='Doctor')
              New_user = AppovedUsers.objects.get(authenticated=True)
              return render(request, 'hospital/create_appointment.html', {'patients': patients, 'doctors': doctors, 'user': New_user})
def index(request):
    employees = Employees.objects.filter(Role='Doctor')
    patients = Patients.objects.all()

    if request.method == 'POST':
        patient = request.POST.get('patient')
        doc = request.POST.get('doctor')
        description = request.POST.get('description')
        date = request.POST.get('app_date')
        time = request.POST.get('app_time')
        pat = Patients.objects.get(id=patient)
        doct = Employees.objects.get(id=doc)
        dateTime = str(date+' ' + time +':00')
        DateTime = datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')

        doctor = Appointment(
            Patient=pat,
            Doctor=doct,
            App_status='schedule',
            App_date=DateTime,
            Date_set=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            Description=description,
            Date_updated=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        doctor.save()
        messages.success(request, 'Appointment Succesfully Booked.')
        return redirect('/index') 
    else:
        New_user = AppovedUsers.objects.get(authenticated=True)
        return render(request, 'hospital/index.html', {'patients': patients, 'doctors': employees, 'user': New_user})


def dashboards(request):
        New_user = AppovedUsers.objects.get(authenticated=True)
        return render(request, 'hospital/dashboards.html', {'user': New_user})

def delete_appointment(request):
        Appointment.objects.get(id=2).delete()
        New_user = AppovedUsers.objects.get(authenticated=True)
        render(request, 'hospital/index.html', {'user': New_user})

def feedback(request):
    patients = Patients.objects.all()
    New_user = AppovedUsers.objects.get(authenticated=True)
    return render(request, 'hospital/feedback.html', {'patients': patients, 'user': New_user})


def doctor_view(request):
    New_user = AppovedUsers.objects.get(authenticated=True)
    return render(request, 'hospital/doctor_view.html', { 'user': New_user})

def delete_user(request, id):
    AppovedUsers.objects.all().delete()
    return  render(request, 'hospital/doctor_view.html')

 

def add_privilege(request, name):
       user = UserPrivileges(Name=name)
       user.save()
       return render(request, 'hospital/doctor_view.html')


def view_appointment(request):
       appointments = Appointment.objects.all()
       New_user = AppovedUsers.objects.get(authenticated=True)
       return render(request, 'hospital/view_appointment.html', {'appointments': appointments, 'user': New_user})