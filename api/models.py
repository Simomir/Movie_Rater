from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from statistics import mean


class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def _get_ratings(self):
        return Rating.objects.filter(movie=self)

    def number_of_ratings(self):
        return len(self._get_ratings())

    def avg_rating(self):
        ratings = self._get_ratings()
        if len(ratings) > 0:
            return mean([int(rating.stars) for rating in ratings])
        else:
            return 0


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)
