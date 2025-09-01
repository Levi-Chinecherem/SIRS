from django.contrib import admin
from taggit.managers import TaggableManager
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    # List display fields
    list_display = (
        "title",
        "owner",
        "category_display",
        "access_level_display",
        "department_display",
        "status_display",
        "upload_date",
        "file_size",
        "security_settings",
    )

    # Filters
    list_filter = (
        "category",
        "access_level",
        "department",
        "status",
        "semantic_indexing",
        "auto_keyword_extraction",
        "watermarked",
        "tags",
    )

    # Search fields
    search_fields = ("title", "description", "tags__name")

    # Ordering
    ordering = ("-upload_date",)

    # Fields to display in the edit form
    fields = (
        "title",
        "owner",
        "file",
        "category",
        "access_level",
        "department",
        "description",
        "tags",
        "is_encrypted",
        "semantic_indexing",
        "auto_keyword_extraction",
        "virus_scanned",
        "watermarked",
        "audit_trail",
        "status",
    )

    # Read-only fields
    readonly_fields = ("upload_date", "size", "encryption_key", "views")

    # List per page
    list_per_page = 25

    # Actions
    actions = [
        "mark_as_completed",
        "enable_semantic_indexing",
        "disable_semantic_indexing",
        "enable_watermarking",
        "disable_watermarking",
    ]

    # Custom display methods
    def category_display(self, obj):
        return obj.get_category_display()

    category_display.short_description = "Category"

    def access_level_display(self, obj):
        return obj.get_access_level_display()

    access_level_display.short_description = "Access Level"

    def department_display(self, obj):
        return obj.get_department_display()

    department_display.short_description = "Department"

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.short_description = "Status"

    def file_size(self, obj):
        return f"{obj.size / 1024 / 1024:.2f} MB" if obj.size else "N/A"

    file_size.short_description = "Size"

    def security_settings(self, obj):
        settings = []
        if obj.is_encrypted:
            settings.append("Encrypted")
        if obj.semantic_indexing:
            settings.append("Semantic Indexing")
        if obj.auto_keyword_extraction:
            settings.append("Auto Keywords")
        if obj.virus_scanned:
            settings.append("Virus Scanned")
        if obj.watermarked:
            settings.append("Watermarked")
        if obj.audit_trail:
            settings.append("Audit Trail")
        return ", ".join(settings) or "None"

    security_settings.short_description = "Security Settings"

    # Custom actions
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status="completed")
        self.message_user(request, f"{updated} document(s) marked as completed.")

    mark_as_completed.short_description = "Mark selected documents as completed"

    def enable_semantic_indexing(self, request, queryset):
        updated = queryset.update(semantic_indexing=True)
        self.message_user(request, f"Enabled semantic indexing for {updated} document(s).")

    enable_semantic_indexing.short_description = "Enable semantic indexing"

    def disable_semantic_indexing(self, request, queryset):
        updated = queryset.update(semantic_indexing=False)
        self.message_user(request, f"Disabled semantic indexing for {updated} document(s).")

    disable_semantic_indexing.short_description = "Disable semantic indexing"

    def enable_watermarking(self, request, queryset):
        updated = queryset.update(watermarked=True)
        self.message_user(request, f"Enabled watermarking for {updated} document(s).")

    enable_watermarking.short_description = "Enable digital watermarking"

    def disable_watermarking(self, request, queryset):
        updated = queryset.update(watermarked=False)
        self.message_user(request, f"Disabled watermarking for {updated} document(s).")

    disable_watermarking.short_description = "Disable digital watermarking"

    # Optimize queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("owner").prefetch_related("tags")

    # Permission checks
    def has_change_permission(self, request, obj=None):
        if obj and obj.owner != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.owner != request.user and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


# Ensure TaggableManager is properly displayed
# admin.site.register(Document, DocumentAdmin)