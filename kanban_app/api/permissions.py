from rest_framework.permissions import BasePermission

class IsBoardOwnerOrMember(BasePermission):
    """Allows owners and members to accsess a board, only owners to delete."""

    def has_object_permission(self, request, view, obj):
        """Checks if the user may access or change this board."""
        is_owner = obj.owner == request.user
        if request.method == 'DELETE':
            return is_owner
        is_member = request.user in obj.members.all()
        return is_owner or is_member
