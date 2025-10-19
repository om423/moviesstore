from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review,
         name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/',
         views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/',
         views.delete_review, name='movies.delete_review'),
    path('<int:id>/rating/submit/',
         views.submit_rating, name='movies.submit_rating'),
    path('local-popularity-map/', views.local_popularity_map, name='movies.local_popularity_map'),
    path("api/region/<int:region_id>/popularity/", views.get_region_popularity, name='movies.get_region_popularity'),
]
