from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    senha_atual = serializers.CharField(required=True)
    senha_nova = serializers.CharField(required=True)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label="Email")
    senha = serializers.CharField(label="Senha", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('senha')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                msg = 'E-mail ou senha, estão incorretos. Tente outra vez.'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Você deve incluir e-mail e senha".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
