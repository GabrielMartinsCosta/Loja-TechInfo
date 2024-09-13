from django.apps import AppConfig

# Configuração padrão do app do django-admin

class TechAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tech_app'
