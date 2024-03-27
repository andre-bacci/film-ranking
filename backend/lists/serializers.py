from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Compilation


class CompilationSerializer(serializers.ModelSerializer):
    owners = UserSerializer(many=True)

    class Meta:
        model = Compilation
        fields = "__all__"


class CompilationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compilation
        fields = ["title"]
