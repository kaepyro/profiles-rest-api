from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    #called every time a request is made, return a bool
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        # We check weather the request is a safe mthod(i.e. get)
        if request.method in permissions.SAFE_METHODS:
            return True

        #if it is not a safe method, we check weather the user is trying
        # to update their own profile
        return obj.id == request.user.id
