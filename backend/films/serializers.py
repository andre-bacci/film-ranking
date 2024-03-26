from rest_framework import serializers

from .models import Credit, Film, Person


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    films = FilmSerializer(many=True)

    class Meta:
        model = Person
        fields = "__all__"


class CreditSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    film = FilmSerializer()

    class Meta:
        model = Credit
        fields = "__all__"
