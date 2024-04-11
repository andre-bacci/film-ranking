from collections import OrderedDict
from typing import Iterable

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, QuerySet
from rest_framework import serializers

from users.serializers import UserSerializer
from utils.lists import are_elements_contiguous, first_element_is_valid

from .models import Compilation, List, ListFilm, Ranking, RankingFilm


class CompilationSerializer(serializers.ModelSerializer):
    owners = UserSerializer(many=True)

    class Meta:
        model = Compilation
        fields = [field.name for field in model._meta.fields]
        fields.extend(["owners"])


class CompilationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compilation
        fields = ["title"]


class ListFilmSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="film.title")
    film_id = serializers.CharField(source="film.tmdb_id")
    directed_by = serializers.CharField(source="film.directed_by")
    written_by = serializers.CharField(source="film.written_by")
    starring = serializers.CharField(source="film.starring")
    release_year = serializers.IntegerField(source="film.release_year")
    poster_url = serializers.CharField(source="film.poster_url")

    class Meta:
        model = ListFilm
        fields = [field.name for field in model._meta.fields]
        fields.extend(
            [
                "title",
                "film_id",
                "directed_by",
                "written_by",
                "starring",
                "release_year",
                "poster_url",
            ]
        )


class ListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    list_films = ListFilmSerializer(many=True)
    compilation = CompilationSerializer()

    class Meta:
        model = List
        fields = [field.name for field in model._meta.fields]
        fields.extend(["list_films"])

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["list_films"] = sorted(
            response["list_films"], key=lambda x: x["ranking"]
        )
        return response


class NestedListFilmSerializer(serializers.ModelSerializer):
    film_id = serializers.CharField(required=True)

    class Meta:
        model = ListFilm
        fields = ["film_id", "ranking", "comment", "grade"]


class ListCreateSerializer(serializers.ModelSerializer):
    list_films = NestedListFilmSerializer(many=True)
    compilation_id = serializers.UUIDField(required=True)

    class Meta:
        model = List
        fields = ["is_ranked", "comment", "list_films", "compilation_id"]

    def validate(self, data):
        try:
            compilation = Compilation.objects.get(id=data.get("compilation_id"))
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Compilation not found")
        if len(data.get("list_films")) > compilation.maximum_list_length:
            raise serializers.ValidationError(
                f"List should not exceed {compilation.maximum_list_length} films"
            )

        if not data.get("is_ranked"):
            return super().validate(data)
        ranking_list = [
            list_film.get("ranking") for list_film in data.get("list_films")
        ]
        if not are_elements_contiguous(ranking_list):
            raise serializers.ValidationError(
                "Film rankings should be unique and contiguous"
            )
        if not first_element_is_valid(ranking_list, 1):
            raise serializers.ValidationError("Rankings should start on 1")
        return super().validate(data)

    def create(self, validated_data: OrderedDict):
        author_id = validated_data.get("author_id")
        data_copy = {**validated_data}
        list_films = data_copy.pop("list_films")

        new_instance = List.objects.create(**data_copy, author_id=author_id)

        for list_film in list_films:
            ListFilm.objects.create(list_id=new_instance.id, **list_film)

        return new_instance

    def update(self, instance: List, validated_data: OrderedDict, **kwargs):
        data_copy = {**validated_data}
        list_films = data_copy.pop("list_films")

        ListFilm.objects.filter(list=instance).delete()

        List.objects.update(**data_copy)

        for list_film in list_films:
            ListFilm.objects.create(list_id=instance.id, **list_film)

        return instance

    """
    Implements specific methods to handle ListFilm data, using the `list` field and the list
    id as an identifier to avoid deleting and recreating records in the database.
    """

    def __init__(self, parent_instance: List):
        super().__init__(
            parent_instance=parent_instance,
            related_model=ListFilm,
            related_queryset=parent_instance.list_films.all(),
            reverse_relationship_name="list",
        )

    def select_objects_to_delete(
        self, related_data: Iterable[OrderedDict]
    ) -> QuerySet[ListFilm]:
        current_related_objects: QuerySet[ListFilm] = self.related_queryset.all()
        incoming_film_ids = [item["film_id"] for item in related_data]
        related_objects_to_delete = current_related_objects.filter(
            ~Q(film_id__in=incoming_film_ids)
        )
        return related_objects_to_delete

    def select_objects_to_update(
        self, related_data: Iterable[OrderedDict]
    ) -> QuerySet[ListFilm]:
        incoming_film_ids = [item["film_id"] for item in related_data]
        objects_to_update = self.related_queryset.filter(film_id__in=incoming_film_ids)
        return objects_to_update

    def map_update_records(self, related_data: Iterable[OrderedDict]) -> dict:
        return {str(item["film_id"]): item for item in related_data}

    def get_object_update_data(
        self, db_item: ListFilm, update_data_map: dict
    ) -> OrderedDict:
        return update_data_map.get(str(db_item.film_id))

    def select_records_to_create(
        self, related_data: Iterable[OrderedDict]
    ) -> Iterable[OrderedDict]:
        current_db_film_ids = self.related_queryset.all().values_list(
            "film_id", flat=True
        )
        records_to_create = [
            item for item in related_data if item["film_id"] not in current_db_film_ids
        ]
        return records_to_create


class RankingFilmSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="film.title")
    directed_by = serializers.CharField(source="film.directed_by")
    written_by = serializers.CharField(source="film.written_by")
    starring = serializers.CharField(source="film.starring")
    release_year = serializers.IntegerField(source="film.release_year")

    class Meta:
        model = RankingFilm
        fields = [field.name for field in model._meta.fields]
        fields.extend(
            ["title", "directed_by", "written_by", "starring", "release_year"]
        )


class RankingSerializer(serializers.ModelSerializer):
    ranking_films = RankingFilmSerializer(many=True)

    class Meta:
        model = Ranking
        fields = [field.name for field in model._meta.fields]
        fields.extend(["ranking_films"])

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["ranking_films"] = sorted(
            response["ranking_films"], key=lambda x: x["position"]
        )
        return response
