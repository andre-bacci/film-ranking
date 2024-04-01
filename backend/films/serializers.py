from rest_framework import serializers

from .models import Film, Person


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
