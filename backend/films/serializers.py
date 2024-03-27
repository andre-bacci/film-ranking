from rest_framework import serializers

from .models import Credit, Film, Person


class NestedPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["imdb_id", "tmdb_id", "name"]


class FilmSerializer(serializers.ModelSerializer):
    directed_by = NestedPersonSerializer(many=True)
    written_by = NestedPersonSerializer(many=True)
    starring = NestedPersonSerializer(many=True)

    class Meta:
        model = Film
        fields = [field.name for field in model._meta.fields]
        fields.extend(["directed_by", "written_by", "starring"])


class PersonSerializer(serializers.ModelSerializer):
    films = FilmSerializer(many=True)

    class Meta:
        model = Person
        fields = [field.name for field in model._meta.fields]


class CreditSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    film = FilmSerializer()

    class Meta:
        model = Credit
        fields = [field.name for field in model._meta.fields]
