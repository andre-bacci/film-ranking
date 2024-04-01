import operator
from typing import Any, Iterable, TypedDict

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from films.models import Film
from utils.models import BaseCreatedUpdatedModel, BaseUUIDModel


class Punctuation(TypedDict):
    points: float
    breakdown: Any
    grades: Iterable[float]
    film_id: str


class Compilation(BaseUUIDModel, BaseCreatedUpdatedModel, models.Model):
    title = models.CharField(max_length=255)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL)
    maximum_list_length = models.IntegerField(default=10)

    def __str__(self) -> str:
        return self.title

    def calculate_ranking(self) -> "Ranking":
        punctuations = {}
        for list in self.lists.all():
            punctuations = list.add_to_punctuation_list(punctuations)

        punctuations = sorted(
            punctuations.values(), key=operator.itemgetter("points"), reverse=True
        )

        ranking = Ranking.objects.create(compilation=self)
        punctuation: Punctuation
        for position, punctuation in enumerate(punctuations):
            average_grade = (
                sum(punctuation["grades"]) / len(punctuation["grades"])
                if len(punctuation["grades"])
                else None
            )
            RankingFilm.objects.create(
                ranking=ranking,
                film_id=punctuation["film_id"],
                average_grade=average_grade,
                points=punctuation["points"],
                points_breakdown=punctuation["breakdown"],
                position=position + 1,
            )

        return ranking


class List(BaseUUIDModel, BaseCreatedUpdatedModel, models.Model):
    compilation = models.ForeignKey(
        to=Compilation, related_name="lists", on_delete=models.CASCADE
    )  # TODO: Allow null
    films = models.ManyToManyField(Film, through="ListFilm")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # TODO: allow unlogged list authors (created by compilation owner)
    is_ranked = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["compilation", "author"]

    def __str__(self) -> str:
        return f"{self.author.get_full_name()} - {self.compilation}"

    @staticmethod
    def exists_by_user_and_compilation(user_id, compilation_id) -> bool:
        return List.objects.filter(
            author_id=user_id, compilation_id=compilation_id
        ).exists()

    def add_to_punctuation_list(self, punctuations):
        film: ListFilm
        for film in self.list_films.all():
            punctuations = film.add_to_punctuation_list(punctuations)
        return punctuations


class ListFilm(BaseUUIDModel, BaseCreatedUpdatedModel, models.Model):
    list = models.ForeignKey(
        to=List, related_name="list_films", on_delete=models.CASCADE
    )
    film = models.ForeignKey(
        to=Film, related_name="list_films", on_delete=models.DO_NOTHING
    )  # TODO: change to CharField
    ranking = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1)]
    )
    comment = models.TextField(blank=True, null=True)
    grade = models.FloatField(blank=True, null=True)
    edited_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Moment at which information relevant to ranking calculation was edited",
    )  # TODO: override save method

    class Meta:
        unique_together = ["film", "list"]

    def __str__(self) -> str:
        return f"{self.film} ({self.list})"

    def save(self, *args, **kwargs):
        if self.list.is_ranked and self.ranking is None:
            raise ValidationError(
                message="Films in a ranked list should all have rankings"
            )
        super().save(*args, **kwargs)

    # TODO: Allow other types of calculations
    @property
    def points(self):
        maximum_list_length = self.list.compilation.maximum_list_length
        if self.list.is_ranked:
            return maximum_list_length - self.ranking + 1
        else:
            return (maximum_list_length + 2) / 2

    def add_to_punctuation_list(self, punctuations):
        # TODO [RNK-46] Adjust ids
        film_id = self.film_id
        punctuation = punctuations.get(film_id)
        punctuations[film_id] = self.add_to_punctuation(punctuation)
        return punctuations

    def add_to_punctuation(self, punctuation=None) -> Punctuation:
        if not punctuation:
            punctuation = {}
            punctuation["points"] = 0
            punctuation["grades"] = []
            punctuation["breakdown"] = {}
            punctuation["film_id"] = self.film_id
        punctuation["points"] += self.points
        if self.grade:
            punctuation["grades"].append(self.grade)
        punctuation["breakdown"] = self.add_to_breakdown(punctuation["breakdown"])
        return punctuation

    def add_to_breakdown(self, breakdown):
        ranking = self.ranking
        if not self.list.is_ranked:
            ranking = "Unranked"
        if ranking not in breakdown:
            breakdown[ranking] = []
        breakdown[ranking].append(self.list.author.get_full_name())
        return breakdown


# Caches a calculated ranking of films
# The Ranking model is needed to keep the information of the calculation datetime
class Ranking(BaseUUIDModel, BaseCreatedUpdatedModel):
    compilation = models.OneToOneField(to=Compilation, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.compilation)


class RankingFilm(BaseUUIDModel):
    ranking = models.ForeignKey(
        to=Ranking, related_name="ranking_films", on_delete=models.CASCADE
    )
    film = models.ForeignKey(
        to=Film, related_name="ranking_films", on_delete=models.CASCADE
    )  # TODO: [RNK-46] Change to CharField
    position = (
        models.IntegerField()
    )  # caches calculated position to avoid having to perform multiple queries for each list viewing
    points = models.FloatField()
    points_breakdown = models.JSONField()
    average_grade = models.FloatField(null=True)

    def __str__(self) -> str:
        return f"{self.film} ({self.ranking})"
