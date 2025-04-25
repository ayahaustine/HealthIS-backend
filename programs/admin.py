from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'created_by')
    search_fields = ('name', 'description', 'id')
    readonly_fields = ('id', 'created_by', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('id', 'name', 'description', 'is_active')
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Automatically set created_by when creating new programs
        """
        if not change:  # Only set created_by when first creating
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        """
        Hide created_by from form fields
        """
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['created_by'].disabled = True
        return form