# Generated by Django 3.2.18 on 2023-10-14 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_auto_20231012_0550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customusers',
            old_name='Username',
            new_name='username',
        ),
    ]