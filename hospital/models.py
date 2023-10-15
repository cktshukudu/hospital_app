from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    staff_number = models.PositiveIntegerField()
    id_number = models.PositiveIntegerField()
    specialization = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    department = models.CharField(max_length=100, choices=[('Dentist', 'Dentistry'), ('Cardiologist', 'Cardiology')])

    def __str__(self):
        return self.name
    
class Department(models.Model):
    Dep_Name = models.CharField(max_length=50, unique=True)
    Description = models.CharField(max_length=10000, unique=True)
    Phone = models.CharField(max_length=13, unique=True)
    Email = models.CharField(max_length=100, unique=True)
    Location = models.CharField(max_length=100, unique=True)
    Date_Added = models.DateTimeField()
    Date_Update = models.DateTimeField()
    isActive = models.BooleanField(default=True)
    def __str__(self):
        return self.Dep_Name
    
class Employees(models.Model):
    Fnames = models.CharField(max_length=100)
    Lname = models.CharField(max_length=100)
    DOB = models.DateField()
    Staff_number = models.CharField(max_length=100,unique=True)
    start_date = models.DateField()
    Role = models.CharField(max_length=100)
    Specialization = models.CharField(max_length=100)
    Department = models.ForeignKey(Department, on_delete=models.PROTECT)
    Rates = models.DecimalField(default=0.0, decimal_places=1, max_digits=3)
    NumOfRates = models.IntegerField(default=0)
    def __str__(self):
        return self.Fnames
    
class UserPrivileges(models.Model):
    Name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.Name

class AppovedUsers(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    CellNumber = models.CharField(max_length=15, unique=True)
    EmailAddress = models.CharField(max_length=50, unique=True)
    SetByUser = models.BooleanField(default=False)
    UserPrivilege = models.ForeignKey(UserPrivileges, on_delete=models.PROTECT)
    Employee = models.ForeignKey(Employees, on_delete=models.PROTECT, unique=True)
    last_login= models.CharField(max_length=50, unique=True)
    authenticated = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    
class Patients(models.Model):
    F_names = models.CharField(max_length=100)
    L_name = models.CharField(max_length=100)
    Gender = models.CharField(max_length=100, choices=[('male', 'Male'), ('female', 'Female')])
    DOB = models.DateField()
    Address = models.CharField(max_length=100)
    Phn_no = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Date_Added = models.DateTimeField()
    Date_Updated = models.DateTimeField()
    def __str__(self):
        return self.F_names
    
class Appointment(models.Model):
    Patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    Doctor = models.ForeignKey(Employees, on_delete=models.PROTECT)
    App_status = models.CharField(max_length=100, default='scheduled',choices=[('scheduled', 'Scheduled' ), ( 'completed', 'Attended'), ( 'cancelled', 'Cancelled')])
    Description = models.CharField(max_length=2500)
    Date_set = models.DateTimeField()
    App_date = models.DateTimeField()
    Date_updated = models.DateTimeField()
    def __str__(self):
        return self.Patient.F_names

class Rooms(models.Model):
    Type = models.CharField(max_length=100)
    Available = models.CharField(max_length=100)
    Identifier = models.CharField(max_length=100)
    Date_Reg = models.DateTimeField()
    Date_Updated = models.DateTimeField()

class Files(models.Model):
    Doc_ID = models.ForeignKey(Employees, on_delete=models.PROTECT)
    Pat_ID = models.ForeignKey(Patients, on_delete=models.PROTECT)
    Symptoms = models.CharField(max_length=2500)
    Diagnosis = models.CharField(max_length=10000)

class Rating(models.Model):
    Patient = models.ForeignKey(Patients, on_delete=models.PROTECT)
    Employee = models.ForeignKey(Employees, on_delete=models.PROTECT)
    Rate = models.IntegerField()
    Feedback = models.CharField(max_length=15000)