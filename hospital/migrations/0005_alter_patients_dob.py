# Generated by Django 4.2.3 on 2023-08-19 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0004_rename_date_patients_dob"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patients",
            name="DOB",
            field=models.DateField(),
        ),
    ]
