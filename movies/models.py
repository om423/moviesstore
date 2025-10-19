from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name

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