from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Set admin site title and header
admin.site.site_title = "SIRS Admin"
admin.site.site_header = "Document Management Administration"
admin.site.index_title = "Admin Dashboard"

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # List display fields
    list_display = (
        'username',
        'email',
        'role_display',
        'department',
        'avatar_initials',
        'is_active',
        'is_staff',
        'last_login',
    )

    # Filters
    list_filter = (
        'role',
        'department',
        'is_active',
        'is_staff',
    )

    # Search fields
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'avatar_initials',
    )

    # Ordering
    ordering = ('-date_joined',)

    # Fields to display in the edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role', 'department', 'avatar_initials')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Read-only fields
    readonly_fields = ('last_login', 'date_joined', 'avatar_initials')

    # List per page
    list_per_page = 25

    # Actions
    actions = [
        'make_admin',
        'make_data_owner',
        'make_general_user',
        'activate_users',
        'deactivate_users',
    ]

    # Custom display methods
    def role_display(self, obj):
        return obj.get_role_display()
    role_display.short_description = 'Role'

    # Custom actions
    def make_admin(self, request, queryset):
        updated = queryset.update(role='admin', is_staff=True)
        self.message_user(request, f"{updated} user(s) set to Admin role.")
    make_admin.short_description = "Set selected users as Admin"

    def make_data_owner(self, request, queryset):
        updated = queryset.update(role='data_owner', is_staff=False)
        self.message_user(request, f"{updated} user(s) set to Data Owner role.")
    make_data_owner.short_description = "Set selected users as Data Owner"

    def make_general_user(self, request, queryset):
        updated = queryset.update(role='general_user', is_staff=False)
        self.message_user(request, f"{updated} user(s) set to General User role.")
    make_general_user.short_description = "Set selected users as General User"

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) activated.")
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) deactivated.")
    deactivate_users.short_description = "Deactivate selected users"

    # Optimize queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

    # Permission checks
    def has_change_permission(self, request, obj=None):
        if obj and obj.role == 'admin' and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.role == 'admin' and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)