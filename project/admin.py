from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name_of_project', 'project_address', 'contact_person_name', 'contact_person_number', 'created_by')
    search_fields = ('name_of_project', 'project_address', 'contact_person_name')
    list_filter = ('created_by',)

    def has_add_permission(self, request):
        return False  # Admin cannot add via admin panel

    def has_change_permission(self, request, obj=None):
        return False  # Admin cannot edit via admin panel

    def has_delete_permission(self, request, obj=None):
        return False  # Admin cannot delete via admin panel
admin.site.register(Project, ProjectAdmin)



