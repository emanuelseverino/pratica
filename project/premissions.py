from datetime import datetime,timezone

from rest_framework.permissions import BasePermission


class ExpirationPermission(BasePermission):

    message = "Atualize seu plano. +55 (22) 99799-0159"

    def has_permission(self, request, view):
        expiration = request.user.expiration
        date_now = datetime.now(timezone.utc)
        if expiration is None:

            return False
        if expiration.date() < date_now.date():
            return False
        return True