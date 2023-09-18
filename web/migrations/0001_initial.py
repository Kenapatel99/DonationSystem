# Generated by Django 4.2.5 on 2023-09-09 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=12)),
                ('contactNo', models.CharField(max_length=10)),
                ('otp', models.CharField(blank=True, max_length=4, null=True)),
            ],
            options={
                'db_table': 'member',
            },
        ),
    ]