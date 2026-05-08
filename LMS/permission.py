from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsLibrarian(BasePermission):

    message = "Only librarians can add books."

    def has_permission(self, request, view):

        return request.user.role == 'LIBRARIAN'
    



class IsStudent(BasePermission):

    message = "Only students can perform this action."

    def has_permission(self, request, view):

        return request.user.role == 'STUDENT'
    



class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user