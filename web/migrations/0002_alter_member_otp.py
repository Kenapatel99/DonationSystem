# Generated by Django 4.2.5 on 2023-09-10 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='otp',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
