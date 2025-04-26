from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_by', 'created_at')
    search_fields = ('name', 'created_by__email')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
