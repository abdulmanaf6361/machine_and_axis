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
        if request.method == 'POST':
            # Prevent access to actions involving 'tool_in_use'
            if 'tool_in_use' in request.data:
                print("Manager access denied for 'tool_in_use' field creation not allowed.")
                return False
            return request.user.groups.filter(name='Manager').exists()
        if request.method in ['PUT', 'PATCH']:
            # Prevent access to actions involving 'tool_in_use'
            return True
        if request.method == 'DELETE':
            return False
        return request.user.groups.filter(name='Manager').exists()


class IsSupervisor(BasePermission):
    """
    Supervisor has restricted permissions based on the access rules.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            # Prevent access to actions involving 'tool_in_use'
            if 'tool_in_use' in request.data:
                print("Supervisor access denied for 'tool_in_use' field creation not allowed.")
                return False
            return request.user.groups.filter(name='Manager').exists()

        if request.method in ['PUT', 'PATCH']:
            return False
        
        if request.method == 'DELETE':
            return False
        
        # Default case
        return request.user.groups.filter(name='Supervisor').exists()


class IsOperator(BasePermission):
    """
    Operator has restricted permissions based on the access rules.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False

        if request.method == 'PATCH':
            if 'tool_in_use' in request.data and len(request.data) == 1:
                return True
            else:
                return False
        if request.method == 'PUT':
            return False
        
        if request.method == 'DELETE':
            return False
        
        # Default case
        return request.user.groups.filter(name='Supervisor').exists()
