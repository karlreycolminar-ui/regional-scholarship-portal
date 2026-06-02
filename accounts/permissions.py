from rest_framework.permissions import BasePermission


class IsApplicant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'applicant'


class IsReviewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'reviewer'


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )


class IsReviewerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('reviewer', 'admin') or request.user.is_superuser


class IsOwnerOrAdmin(BasePermission):
    """Object-level: only owner or admin can access"""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        # Anti-IDOR: check ownership
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
