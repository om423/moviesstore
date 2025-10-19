from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

    def get_average_rating(self):
        avg = self.rating_set.aggregate(Avg('stars'))['stars__avg']
        return round(avg, 1) if avg is not None else None

    def get_rating_count(self):
        return self.rating_set.count()


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
                              on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    stars = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),])
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.movie.name} - {self.stars} stars"

class GeographicRegion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    lattitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class MoviePopularity(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    purchase_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    geographic_region = models.ForeignKey(GeographicRegion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'geographic_region')

    def __str__(self):
        return f"{self.movie.name} in {self.geographic_region.name}"
