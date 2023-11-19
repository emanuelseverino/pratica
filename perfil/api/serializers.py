from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from user.models import User


class PerfilSerializer(serializers.ModelSerializer):
    foto = Base64ImageField(required=False, source='image')
    usuario = serializers.CharField(source='username')
    nome = serializers.CharField(source='first_name')
    sobrenome = serializers.CharField(source='last_name')
    latitude = serializers.CharField(source='lat')
    longitude = serializers.CharField(source='long')

    class Meta:
        model = User
        fields = ['id', 'foto', 'usuario', 'nome', 'sobrenome', 'email', 'latitude', 'longitude']

    def validate(self, data):
        email = data['email']
        if email:
            raise serializers.ValidationError('Você não pode atualizar seu e-mail')


    def get_object(self):
        return User.objects.get(email=self)