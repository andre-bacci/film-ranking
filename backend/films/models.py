from django.db import models
from django.db.models.query import QuerySet

from utils.models import BaseCreatedUpdatedModel, BaseUUIDModel


class Film(BaseCreatedUpdatedModel, models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=12, blank=True, null=True)
    title = models.CharField(max_length=512)
    original_title = models.CharField(max_length=512, blank=True, null=True)
    pt_br_title = models.CharField(max_length=512, blank=True, null=True)
    release_date = models.DateField()
    runtime = models.IntegerField(null=True)
    synopsis = models.TextField(blank=True, null=True)

    @property
    def release_year(self) -> str:
        return str(self.release_date.year) if self.release_date.year else None

    @property
    def directed_by_queryset(self) -> "QuerySet[Person]":
        return self.get_credited_people_by_role(role=CreditRoleOptions.DIRECTOR)

    @property
    def directed_by(self) -> str:
        return Person.convert_person_queryset_to_string(self.directed_by_queryset)

    @property
    def written_by_queryset(self) -> "QuerySet[Person]":
        return self.get_credited_people_by_role(role=CreditRoleOptions.WRITER)

    @property
    def written_by(self) -> str:
        return Person.convert_person_queryset_to_string(self.written_by_queryset)

    @property
    def starring_queryset(self) -> "QuerySet[Person]":
        return self.get_credited_people_by_role(role=CreditRoleOptions.ACTOR)

    @property
    def starring(self) -> str:
        return Person.convert_person_queryset_to_string(self.starring_queryset)

    def get_credited_people_by_role(self, role) -> "QuerySet[Person]":
        # TODO: Make query more efficient
        credits_by_role: QuerySet[Credit] = self.credits.filter(role__iexact=role)
        return Person.objects.filter(credits__in=credits_by_role)

    def __str__(self) -> str:
        return f"{self.title} ({self.release_year})"


class Person(BaseCreatedUpdatedModel, models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=12, blank=True, null=True)
    name = models.CharField(max_length=512)
    bio = models.TextField(blank=True, null=True)
    films = models.ManyToManyField(
        "Film", through="Credit", related_name="credited_people"
    )
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def convert_person_queryset_to_string(queryset: "QuerySet[Person]") -> str:
        return ", ".join(list(queryset.values_list("name", flat=True)))


class CreditRoleOptions(models.TextChoices):
    ACTOR = "actor"
    DIRECTOR = "director"
    WRITER = "writer"


class Credit(BaseUUIDModel, BaseCreatedUpdatedModel, models.Model):
    person = models.ForeignKey(
        "Person", related_name="credits", on_delete=models.CASCADE
    )
    film = models.ForeignKey("Film", related_name="credits", on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=CreditRoleOptions.choices)

    def __str__(self) -> str:
        return f"{self.person} - {self.film} ({self.role})"

    class Meta:
        unique_together = ["person", "film", "role"]
