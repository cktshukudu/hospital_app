# Generated by Django 3.2.18 on 2023-10-14 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_alter_customusers_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppovedUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('CellNumber', models.CharField(max_length=15, unique=True)),
                ('EmailAddress', models.CharField(max_length=50, unique=True)),
                ('SetByUser', models.BooleanField(default=False)),
                ('last_login', models.CharField(max_length=50, unique=True)),
                ('Employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.employees', unique=True)),
                ('UserPrivilege', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.userprivileges')),
            ],
        ),
    ]