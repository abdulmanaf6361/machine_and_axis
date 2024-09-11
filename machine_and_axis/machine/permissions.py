from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    """
    Superadmin has all permissions: Create, Read, Update, Delete.
    """
    def has_permission(self, request, view):
        return request.user.is_staff  # Assuming superadmins have is_staff=True

class IsManager(BasePermission):
    """
    Manager has restricted permissions based on the access rules.
    """
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH']:
            return request.user.groups.filter(name='Manager').exists() and view.action != 'tool_in_use'
        if request.method == 'DELETE':
            return False
        return request.user.groups.filter(name='Manager').exists()

class IsSupervisor(BasePermission):
    """
    Supervisor has restricted permissions based on the access rules.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.groups.filter(name='Supervisor').exists()
        if request.method in ['PUT', 'PATCH'] and view.action == 'tool_in_use':
            return False
        if request.method == 'DELETE' and view.action == 'tool_in_use':
            return True
        return request.user.groups.filter(name='Supervisor').exists()

class IsOperator(BasePermission):
    """
    Operator has restricted permissions based on the access rules.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.groups.filter(name='Operator').exists() and view.action == 'tool_in_use'
        if request.method == 'DELETE':
            return False
        return request.user.groups.filter(name='Operator').exists()
