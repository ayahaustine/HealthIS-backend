from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'county', 'programs_list', 'is_active')
    list_filter = ('gender', 'county', 'is_active', 'created_by')
    search_fields = ('first_name', 'last_name', 'id', 'phone_number')
    filter_horizontal = ('programs',)
    readonly_fields = ('id', 'created_by', 'created_at')
    
    fieldsets = (
        ('Personal Info', {
            'fields': (
                'first_name', 'last_name', 'date_of_birth', 'gender',
                'phone_number', 'county', 'sub_county'
            )
        }),
        ('Program Enrollment', {
            'fields': ('programs',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Audit Info', {
            'fields': ('id', 'created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    def programs_list(self, obj):
        return ", ".join([p.name for p in obj.programs.all()])
    programs_list.short_description = 'Enrolled Programs'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)