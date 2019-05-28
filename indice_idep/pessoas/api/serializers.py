from pessoas.models import ServidorUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServidorUser
        fields = ('rf', 'password', 'ano_nasc',)
