from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'gender', 'created_by', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone_number', 'created_by__email')
    list_filter = ('gender', 'created_at')
    ordering = ('-created_at',)
