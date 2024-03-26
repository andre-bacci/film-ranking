from django.db import models
from django.db.models.query import QuerySet

from utils.models import BaseCreatedUpdatedModel, BaseUUIDModel


class Film(BaseCreatedUpdatedModel, models.Model):
    imdb_id = models.CharField(max_length=12, primary_key=True)
    tmdb_id = models.IntegerField(blank=True, null=True)
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
    def directed_by(self) -> "QuerySet[Person]":
        return self.get_credits_by_role(role="director")

    @property
    def written_by(self) -> "QuerySet[Person]":
        return self.get_credits_by_role(role="writer")

    @property
    def starring(self) -> "QuerySet[Person]":
        return self.get_credits_by_role(role="actor")

    def get_credits_by_role(self, role) -> "QuerySet[Person]":
        credits: QuerySet[Credit] = self.credits
        return credits.filter(role__iexact=role).values_list("person", flat=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.release_year})"


class Person(BaseCreatedUpdatedModel, models.Model):
    imdb_id = models.CharField(max_length=12, primary_key=True)
    tmdb_id = models.IntegerField(blank=True, null=True)
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


class Credit(BaseUUIDModel, BaseCreatedUpdatedModel, models.Model):
    person = models.ForeignKey(
        "Person", related_name="credits", on_delete=models.CASCADE
    )
    film = models.ForeignKey("Film", related_name="credits", on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.person} - {self.film} ({self.role})"

    class Meta:
        unique_together = ["person", "film", "role"]
