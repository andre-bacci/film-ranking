from typing import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Credit, CreditRoleOptions, Film, Person


class NestedPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["imdb_id", "tmdb_id", "name"]


class FilmSerializer(serializers.ModelSerializer):
    directed_by = NestedPersonSerializer(many=True, source="directed_by_queryset")
    written_by = NestedPersonSerializer(many=True, source="written_by_queryset")
    starring = NestedPersonSerializer(many=True, source="starring_queryset")
    release_year = serializers.IntegerField()

    class Meta:
        model = Film
        fields = [field.name for field in model._meta.fields]
        fields.extend(["directed_by", "written_by", "starring", "release_year"])


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


class PersonSaveSerializer(serializers.ModelSerializer):
    imdb_id = serializers.CharField(max_length=12, allow_null=True, allow_blank=True)
    tmdb_id = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=512)
    bio = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    date_of_death = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Person
        fields = [
            "imdb_id",
            "tmdb_id",
            "name",
            "bio",
            "date_of_birth",
            "date_of_death",
        ]

    def save(self, validated_data: OrderedDict):
        return Person.objects.create(**validated_data)


class FilmSaveSerializer(serializers.ModelSerializer):
    imdb_id = serializers.CharField(max_length=12)
    tmdb_id = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.CharField(max_length=512)
    original_title = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    pt_br_title = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    release_date = serializers.DateField()
    runtime = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Film
        fields = [
            "imdb_id",
            "tmdb_id",
            "title",
            "original_title",
            "pt_br_title",
            "release_date",
            "runtime",
            "synopsis",
        ]

    def save(self, validated_data: OrderedDict) -> Film:
        return Film.objects.create(**validated_data)
