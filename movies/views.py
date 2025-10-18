from django.shortcuts import render, redirect, get_object_or_404
from .models import MoviePopularity, Movie, Review, GeographicRegion
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import JsonResponse

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    default_region = GeographicRegion.objects.filter(name='North America').first()
    if not default_region:
        default_region = GeographicRegion.objects.first()

    if default_region:
        popularity, created = MoviePopularity.objects.get_or_create(
            movie=movie,
            geographic_region=default_region,
            defaults={'purchase_count': 0, 'view_count': 0})
        popularity.view_count += 1
        popularity.save()

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def local_popularity_map(request):
    template_data = {}
    template_data['title'] = 'Local Popularity Map'
    region = GeographicRegion.objects.all()
    template_data['regions'] = region
    return render(request, 'movies/local_popularity_map.html', {'template_data': template_data})

def get_region_popularity(request, region_id):
    try:
        region = get_object_or_404(GeographicRegion, id=region_id)
        popularities = MoviePopularity.objects.filter(geographic_region=region).order_by(
            '-purchase_count', '-view_count')[:10]
        data = {
            "region_name": region.name,
            "movies": []
        }
        for popularity in popularities:
            movie_data = {
                "id": popularity.movie.id,
                "name": popularity.movie.name,
                "purchase_count": popularity.purchase_count,
                "view_count": popularity.view_count,
                "total_activity": popularity.purchase_count + popularity.view_count,
                "image_url": popularity.movie.image.url if popularity.movie.image else None
            }

            data["movies"].append(movie_data)

        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)