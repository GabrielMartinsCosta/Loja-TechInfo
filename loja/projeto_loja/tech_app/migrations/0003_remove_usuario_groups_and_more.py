# Generated by Django 5.0.6 on 2024-06-26 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tech_app', '0002_usuario_groups_usuario_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user_permissions',
        ),
    ]
