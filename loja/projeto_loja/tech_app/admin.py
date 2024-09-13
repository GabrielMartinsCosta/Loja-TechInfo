from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Produto

class CustomUserAdmin(BaseUserAdmin):
    # Fields to display in the admin list view
    list_display = ['email', 'nome', 'cpf', 'is_staff', 'is_superuser']

    # Filter options in the admin panel
    list_filter = ['is_staff', 'is_active']

    # Fields to display as horizontal filters
    filter_horizontal = []

    # Ordering options for the admin panel
    ordering = ['email']

    # Define fieldsets to control layout in admin panel
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'cpf')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'cpf', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'nome', 'cpf')
    ordering = ('email',)

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Produto)
