from django.contrib import admin
from request_handler.models import AllowedRequest


class AllowedRequestAdmin(admin.ModelAdmin):
    """
    Custom django admin panel for managing and configuring available requests.
    """
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


# register model in admin panel
admin.site.register(AllowedRequest, AllowedRequestAdmin)
