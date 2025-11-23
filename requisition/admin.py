# A - Import Required Modules
from django.contrib import admin
from .models import RequisitionProfile, BasicInformation, RequisitionItem

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

# D - RequisitionProfile Admin
@admin.register(RequisitionProfile)
class RequisitionProfileAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']
    ordering = ['user__username']

# E - BasicInformation Admin
@admin.register(BasicInformation)
class BasicInformationAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['requisition_no', 'project_name', 'requisition_date', 'prepared_by', 'delivery_date']
    list_filter = ['requisition_date', 'delivery_date']
    search_fields = ['requisition_no', 'project_name', 'prepared_by']
    ordering = ['-requisition_date']

# F - RequisitionItem Admin
@admin.register(RequisitionItem)
class RequisitionItemAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = [
        'PR_no', 'project_name_fpr', 'name_of_resource', 'quantity',
        'unit_price', 'total_amount', 'status', 'team',
        'created_by', 'created_at', 'updated_by', 'updated_at'
    ]
    list_filter = ['status', 'team', 'created_by', 'updated_by']
    search_fields = ['PR_no', 'name_of_resource', 'created_by__username', 'updated_by__username']
    ordering = ['-created_at']

