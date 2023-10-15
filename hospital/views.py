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
        return render(request, 'hospital/ratings.html', {'employees': employees, 'patients': patients, 'rate': rate_star})

def doctors_list(request):
       doctors = Employees.objects.filter(Role='Doctor')
       return render(request, 'hospital/doctor_list.html', {'doctors': doctors})

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
                            return render(request, 'hospital/admin1.html')
                     else:
                            messages.error(request, 'Incorrect username/password')
                            return render(request, 'hospital/login.html')
               except AppovedUsers.DoesNotExist:
                      messages.error(request, 'Incorrect username/password')
                      return render(request, 'hospital/login.html')
        else:
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
                     new_user = AppovedUsers(username=username, EmailAddress=email, password=password, CellNumber=cellnumber, Employee=staff_number, UserPrivilege=chosenPrivilege, last_login=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), key='')
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
        return render(request, 'hospital/admin1.html',{'ratings':ratings})

def create_emp(request):
        departments = Department.objects.all()
        if request.method == 'POST':
                name = request.POST.get('names')
                l_name = request.POST.get('l_name')
                DOB = request.POST.get('DOB')
                staff = request.POST.get('staff_no')
                start = request.POST.get('start_date')
                role = request.POST.get('role')
                specialization = request.POST.get('specialization')
                department = request.POST.get('department')
                dep = Department.objects.get(id=department)
                employee = Employees(Fnames=name, Lname=l_name, DOB=DOB, Staff_number=staff, start_date=start, Role=role, Specialization=specialization, Department=dep)
                employee.save()
                return render(request, 'hospital/view_emp.html')
        else:
                return render(request, 'hospital/create_emp.html', {'departments': departments})
        
def details(request, link):
       doctor = Employees.objects.get(id=link)
       return render(request, 'hospital/doctor-details.html', {'doctor': doctor})

def view_emp(request):
       employees = Employees.objects.all()
       return render(request, 'hospital/view_emp.html', {'employees': employees})

def create_dep(request):
        if request.method == 'POST':
                name = request.POST.get('dep_name')
                description = request.POST.get('description')
                phone = request.POST.get('cellphone')
                email = request.POST.get('email')
                location = request.POST.get('location')
                department = Department(Dep_Name= name, Description=description, Phone=phone, Email=email, Location=location, Date_Added= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), Date_Update=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                department.save()
                return render(request, 'hospital/view_dep.html')
        else:
                return render(request, 'hospital/create_dep.html')

def view_dep(request):
       departments = Department.objects.all()
       return render(request, 'hospital/view_dep.html', {'departments': departments})

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
              return redirect('/')
       else:
              return render(request, 'hospital/create_patient.html')
       
def create_appointment(request):
       if request.method == 'POST':
              patient = request.POST.get('patient')
              pat_data = Patients.objects.get(id=patient)
              doctor = request.POST.get('doctor')
              doc_data = Employees.objects.get(id=doctor)
              description = request.POST.get('description')
              app_date = request.POST.get('app_date')
              print(app_date)
        #       appointment = Appointment(Patient=pat_data, Doctor=doc_data, Description=description, Date_set=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), App_date=app_date, Date_updated=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #       appointment.save()
              return render(request, 'hospital/create_appointment.html', {'patients': patients, 'doctors': doctors})
       else:
              patients = Patients.objects.all()
              doctors = Employees.objects.filter(Role='Doctor')
              return render(request, 'hospital/create_appointment.html', {'patients': patients, 'doctors': doctors})
def index(request):
    employees = Employees.objects.filter(Role='Doctor')
    patients = Patients.objects.all()

    if request.method == 'POST':
        patient = request.POST.get('patient')
        doc = request.POST.get('doctor')
        description = request.POST.get('description')
        date = request.POST.get('app_date')
        pat = Patients.objects.get(id=patient)
        doct = Employees.objects.get(id=doc)
 

        doctor = Appointment(
            Patient=pat,
            Doctor=doct,
            App_status='schedule',
            App_date=date,
            Date_set=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            Description=description,
            Date_updated=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        doctor.save()

        return redirect('/index') 
    else:
        return render(request, 'hospital/index.html', {'patients': patients, 'doctors': employees})


def dashboards(request):
        return render(request, 'hospital/dashboards.html')

def delete_appointment(request):
        Appointment.objects.get(id=2).delete()
        render(request, 'hospital/index.html')

def feedback(request):
    patients = Patients.objects.all()
    return render(request, 'hospital/feedback.html', {'patients': patients})


def patient(request):
    return render(request, 'hospital/patient.html')

def doctor_view(request):
    return render(request, 'hospital/doctor_view.html')

def delete_user(request, id):
    AppovedUsers.objects.all().delete()
    return  render(request, 'hospital/doctor_view.html')

 

def add_privilege(request, name):
       user = UserPrivileges(Name=name)
       user.save()
       return render(request, 'hospital/doctor_view.html')
