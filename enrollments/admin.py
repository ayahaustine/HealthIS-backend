from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'program', 'status', 'enrollment_date', 'enrolled_by')
    list_filter = ('status', 'enrollment_date', 'program')
    search_fields = ('client__first_name', 'client__last_name', 'program__name')
    raw_id_fields = ('client', 'program')
    readonly_fields = ('enrolled_by', 'enrollment_date')

    fieldsets = (
        (None, {
            'fields': ('client', 'program', 'status')
        }),
        ('Dates', {
            'fields': ('enrollment_date', 'completed_date'),
            'classes': ('collapse',)
        }),
        ('Additional Info', {
            'fields': ('notes', 'enrolled_by'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.enrolled_by = request.user
        super().save_model(request, obj, form, change)