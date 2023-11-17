from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    senha_atual = serializers.CharField(required=True)
    senha_nova = serializers.CharField(required=True)
