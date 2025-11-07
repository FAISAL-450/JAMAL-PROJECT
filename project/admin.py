# A - Import Required Modules
from django.contrib import admin
from .models import Project, ProjectProfile

# B - Azure Admin Email
AZURE_ADMIN_EMAIL = 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Mixin: Restrict Admin Access to Azure Admin
class AzureAdminOnlyMixin:
    def has_module_permission(self, request):
        return request.user.email == AZURE_ADMIN_EMAIL

    def has_view_permission(self, request, obj=None):
        return request.user.email == AZURE_ADMIN_EMAIL

    def has_change_permission(self, request, obj=None):
        return request.user.email == AZURE_ADMIN_EMAIL

    def has_delete_permission(self, request, obj=None):
        return request.user.email == AZURE_ADMIN_EMAIL

    def has_add_permission(self, request):
        return request.user.email == AZURE_ADMIN_EMAIL

# D - ProjectProfile Admin
@admin.register(ProjectProfile)
class ProjectProfileAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']

# E - Project Admin
@admin.register(Project)
class ProjectAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['name_of_project', 'project_address', 'contact_person_name', 'contact_person_number', 'team', 'created_by', 'created_at']
    list_filter = ['team', 'created_by']
    search_fields = ['name_of_project', 'project_address', 'contact_person_name', 'created_by__username']
    readonly_fields = ['created_by', 'created_at']





