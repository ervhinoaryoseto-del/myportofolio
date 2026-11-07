from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )

class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    message = "Only the portfolio owner or an Editor can update projects."

    def has_permission(self, request, view):
        user = request.user

        if request.method in SAFE_METHODS:
            return True
        if not user or not user.is_authenticated:
            return False
        
        # Editor dan Superuser boleh mengubah data
        if request.method in ("PUT", "PATCH"):
            return (
                user.is_superuser or user.groups.filter(name="Editor").exists()
            )

        if request.method in ("POST", "DELETE"):
            return user.is_superuser

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in SAFE_METHODS:
            return True

        if not user or not user.is_authenticated:
            return False

        if request.method in ("PUT", "PATCH"):
            return (
                user.is_superuser
                or user.groups.filter(name="Editor").exists()
            )

        if request.method == "DELETE":
            return user.is_superuser

        return False
