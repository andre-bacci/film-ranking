from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import IntegrityError, models

from films.models import Film
from utils.models import BaseCreatedUpdatedModel, BaseUUIDModel


class Compilation(BaseUUIDModel, BaseCreatedUpdatedModel, models.Model):
    title = models.CharField(max_length=255)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self) -> str:
        return self.title


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


class ListFilm(BaseUUIDModel, BaseCreatedUpdatedModel, models.Model):
    list = models.ForeignKey(
        to=List, related_name="list_films", on_delete=models.CASCADE
    )
    film = models.ForeignKey(
        to=Film, related_name="list_films", on_delete=models.DO_NOTHING
    )
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


# Caches a calculated ranking of films
# The Ranking model is needed to keep the information of the calculation datetime
class Ranking(BaseUUIDModel, BaseCreatedUpdatedModel):
    compilation = models.OneToOneField(to=Compilation, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.compilation)


class RankingFilm(BaseUUIDModel):
    ranking = models.ForeignKey(to=Ranking, on_delete=models.CASCADE)
    film = models.ForeignKey(
        to=Film, related_name="ranking_films", on_delete=models.CASCADE
    )  # TODO: Change to DO_NOTHING
    position = (
        models.IntegerField()
    )  # caches calculated position to avoid having to perform multiple queries for each list viewing
    points = models.FloatField()
    points_breakdown = models.TextField()

    def __str__(self) -> str:
        return f"{self.film} ({self.ranking})"
