# Generated by Django 4.2.4 on 2023-08-07 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=16)),
            ],
        ),
    ]
