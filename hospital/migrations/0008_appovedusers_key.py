# Generated by Django 3.2.18 on 2023-10-14 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0007_appovedusers_authenticated'),
    ]

    operations = [
        migrations.AddField(
            model_name='appovedusers',
            name='key',
            field=models.CharField(default='', max_length=50000, unique=True),
            preserve_default=False,
        ),
    ]