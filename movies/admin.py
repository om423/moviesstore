from django.contrib import admin
from .models import Movie, Review, Rating


class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie', 'stars', 'date')
    list_filter = ('stars', 'date')
    search_fields = ('user__username', 'movie__name')
    oredering = ('-date',)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
