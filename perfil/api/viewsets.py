from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet

from perfil.api.serializers import PerfilSerializer
from project.premissions import ExpirationPermission
from user.models import User


class PerfilViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated, ExpirationPermission]
    authentication_classes = [TokenAuthentication, ]
    renderer_classes = [JSONRenderer,]

    def get_object(self):
        return User.objects.get(email=self.request.user.email)
