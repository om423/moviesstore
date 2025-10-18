from django.contrib import admin
from .models import Movie, Review, GeographicRegion, MoviePopularity
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


class GeographicRegionAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class MoviePopularityAdmin(admin.ModelAdmin):
    list_display = ['movie', 'region', 'purchase_count', 'view_count', 'last_updated']
    list_filter = ['region', 'last_updated']
    search_fields = ['movie__name', 'region__name']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(GeographicRegion, GeographicRegionAdmin)
admin.site.register(MoviePopularity, MoviePopularityAdmin)
