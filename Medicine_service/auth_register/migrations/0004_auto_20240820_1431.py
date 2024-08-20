# Generated by Django 3.2.2 on 2024-08-20 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_remove_doctor_account'),
        ('user', '0003_auto_20240820_1431'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('auth_register', '0003_alter_account_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='doctor_data',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_data', to='doctor.doctor', verbose_name='Данные врача'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_data',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_data', to='user.user', verbose_name='Данные пользователя'),
        ),
        migrations.AlterField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='account_set', to='auth.Group', verbose_name='Группы'),
        ),
        migrations.AlterField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='account_set', to='auth.Permission', verbose_name='Разрешения'),
        ),
    ]
