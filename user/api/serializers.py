from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    senha = serializers.CharField(write_only=True, required=True, validators=[validate_password], source='password')
    csenha = serializers.CharField(write_only=True, required=True, source='password2')
    nome = serializers.CharField(required=True, source='first_name')
    sobrenome = serializers.CharField(required=True, source='last_name')

    class Meta:
        model = User
        fields = ('senha', 'csenha', 'email', 'nome', 'sobrenome')

    def validate(self, attrs):
        if attrs.get('senha') != attrs.get('csenha'):
            raise serializers.ValidationError({"senha": "Suas senhas precisam ser iguais."})

        return attrs

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


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
