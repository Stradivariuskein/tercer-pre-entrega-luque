# Generated by Django 4.2.4 on 2023-08-08 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contactos', '0002_rename_username_user_lastname_user_name'),
        ('agenda', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turn',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contactos.user'),
        ),
    ]
