# Generated by Django 5.0.6 on 2024-06-27 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech_app', '0003_remove_usuario_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
