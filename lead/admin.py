from django.contrib import admin
from .models import Lead
from customerdetailed.models import Profile  # ✅ import only, no registration

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_company', 'get_created_by', 'get_team', 'created_at']
    list_filter = ['customer_name__team', 'customer_name__created_by']
    search_fields = ['customer_name__name', 'customer_company', 'customer_name__created_by__username']

    def get_created_by(self, obj):
        return obj.customer_name.created_by.username if obj.customer_name and obj.customer_name.created_by else "-"
    get_created_by.short_description = 'Created By'

    def get_team(self, obj):
        return obj.customer_name.team if obj.customer_name else "-"
    get_team.short_description = 'Team'
