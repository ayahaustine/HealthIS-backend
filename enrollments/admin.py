from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'program', 'created_by', 'enrolled_at')
    search_fields = ('client__first_name', 'client__last_name', 'program__name', 'created_by__email')
    list_filter = ('enrolled_at',)
    ordering = ('-enrolled_at',)
