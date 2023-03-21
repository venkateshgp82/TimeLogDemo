from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        #check user is editing his own record
        # Write permissions are only allowed to the owner of the object.
        return request.user == request.data.get('user')