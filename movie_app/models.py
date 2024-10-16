from django.db import models
from statistics import mean

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def movie_count(self):
        return self.movies.count()


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title

    @property
    def review_list(self):
        return [i.text for i in self.reviews.all()]

    @property
    def rating(self):
        ratings = [review.stars for review in self.reviews.all()]
        if ratings:
            return mean(ratings)
        return None


STAR_CHOICES = (
    (i, '*' * i) for i in range(1, 6)
)


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    stars = models.FloatField(choices=STAR_CHOICES, default=0)

    def __str__(self):
        return self.text
