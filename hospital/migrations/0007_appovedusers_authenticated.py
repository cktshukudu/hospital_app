# Generated by Django 3.2.18 on 2023-10-14 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_appovedusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='appovedusers',
            name='authenticated',
            field=models.BooleanField(default=False),
        ),
    ]
