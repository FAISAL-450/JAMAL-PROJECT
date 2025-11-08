from django.contrib import admin
from .models import Project

AZURE_ADMIN_EMAIL = 'admin@dzignscapeprofessionals.onmicrosoft.com'

class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name_of_project',
        'project_address',
        'contact_person_name',
        'contact_person_number',
        'created_by',
    )
    search_fields = (
        'name_of_project',
        'project_address',
        'contact_person_name',
    )
    list_filter = ('created_by',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.email.lower() == AZURE_ADMIN_EMAIL:
            return qs  # Admin sees all projects
        return qs.filter(created_by=request.user)  # Team members see only their own

    def has_add_permission(self, request):
        return False  # Disable add in admin

    def has_change_permission(self, request, obj=None):
        return False  # Disable edit in admin

    def has_delete_permission(self, request, obj=None):
        return False  # Disable delete in admin

admin.site.register(Project, ProjectAdmin)






