from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    """Allows owners and members to access a board, only owners to delete."""

    def has_object_permission(self, request, view, obj):
        """Checks if the user may access or change this board."""
        is_owner = obj.owner == request.user
        if request.method == 'DELETE':
            return is_owner
        is_member = request.user in obj.members.all()
        return is_owner or is_member


class IsTaskBoardMember(BasePermission):
    """Allows board members to edit a task, only creator or owner to delete."""

    def has_object_permission(self, request, view, obj):
        """Checks if the user may change or delete this task."""
        board = obj.board
        is_owner = board.owner == request.user
        if request.method == 'DELETE':
            return is_owner or obj.created_by == request.user
        is_member = request.user in board.members.all()
        return is_owner or is_member


class IsCommentAuthor(BasePermission):
    """Allows only the author to delete a comment."""

    def has_object_permission(self, request, view, obj):
        """Checks if the user wrote this comment."""
        return obj.author == request.user