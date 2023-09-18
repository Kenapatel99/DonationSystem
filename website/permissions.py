from rest_framework.permissions import BasePermission
import logging

# Logger variables to be used for logging
from website.settings import SOURCE_TOKEN

info_logger = logging.getLogger('api_info_logger')
error_logger = logging.getLogger('api_db_error_logger')

# has_permission() is for the user-level permission
# has_object_permission() is object-level permission.

class IsValidSourceAndToken(BasePermission):
    message = "You are not authorized to access this API."  # custom error message

    def has_permission(self, request, view):
        source_system = request.data.get("source_system", "")
        auth_token = request.data.get("auth_token", "")
        is_valid = False
        if source_system in SOURCE_TOKEN and SOURCE_TOKEN[source_system] == auth_token:
            is_valid = True

        return is_valid
