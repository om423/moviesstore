from django.core.management.base import BaseCommand
from movies.models import Movie, GeographicRegion, MoviePopularity
import random

class Command(BaseCommand):
    help = 'Populate database with sample geographic regions and movie popularity data'

    def handle(self, *args, **options):
        regions_data = [
            {'name': "North America", "lattitude": 45.0, "longitude": -100.0, "description": "United States and Canada"},
            {'name': "Europe", "lattitude": 50.0, "longitude": 10.0, "description": "United Kingdom and Europe"},
            {'name': "Asia", "lattitude": 30.0, "longitude": 120.0, "description": "China and Japan"},
            {'name': "Africa", "lattitude": -10.0, "longitude": 30.0, "description": "Nigeria and South Africa"},
            {'name': "Australia", "lattitude": -25.0, "longitude": 135.0, "description": "Australia"},
            {'name': "South America", "lattitude": -10.0, "longitude": -60.0, "description": "Brazil and Argentina"},
        ]
    
        regions = []
        for region_data in regions_data:
            region, created = GeographicRegion.objects.get_or_create(
                name = region_data['name'],
                defaults = region_data
            )
            regions.append(region)
            if created:
                self.stdout.write(f"Created region: {region.name}")
        movies = Movie.objects.all()
        if not movies.exists():
            self.stdout.write(self.style.WARNING("No movies found. Please create some movies first."))
            return
        
        for region in regions:
            for movie in movies:
                purchase_count = random.randint(0, 50)
                view_count = random.randint(0, 200)

                popularity, created = MoviePopularity.objects.get_or_create(
                    movie = movie,
                    geographic_region = region,
                    defaults = {'purchase_count': purchase_count, 'view_count': view_count}
                )
                if created:
                    self.stdout.write(f"Created popularity for {movie.name} in {region.name}")
        self.stdout.write(self.style.SUCCESS("Successfully populated database with sample geographic regions and movie popularity data"))