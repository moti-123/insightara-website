from django.contrib import admin
from django.utils.html import format_html
from .models import TeamMember, Project, ContactMessage


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role_category", "job_title", "display_order", "is_active", "photo_preview")
    list_filter = ("role_category", "is_active")
    search_fields = ("full_name", "job_title")
    list_editable = ("display_order", "is_active")

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = "Photo"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client_name", "status", "added_by", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "client_name", "tools_used")

    def save_model(self, request, obj, form, change):
        # Auto-record who added the project, unless it's already set
        if not obj.added_by_id:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "submitted_at", "is_read")
    list_filter = ("is_read", "submitted_at")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("name", "email", "company", "message", "submitted_at")

    def has_add_permission(self, request):
        # Inquiries only come from the public contact form, not created in admin
        return False


admin.site.site_header = "Insightara Admin"
admin.site.site_title = "Insightara Admin"
admin.site.index_title = "Manage your site"
