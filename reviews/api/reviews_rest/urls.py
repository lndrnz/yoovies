from django.urls import path
from .views import api_list_reviews, api_show_review, api_list_movies, api_list_reviews_by_imdb_id

urlpatterns = [
    path("movies/", api_list_movies, name="list_movies"),
    path("reviews/<str:imdb_id>/", api_list_reviews_by_imdb_id, name="list_reviews"),
    path("reviews/<int:movie_id>/", api_list_reviews, name="review_by_id"),
    # path("reviews/<str:movie_imdb>/", api_list_reviews, name="movie_by_imdb"),


    path("create/<int:movie_id>/", api_list_reviews, name="create"),


    path("reviews/edit/<int:pk>/", api_show_review, name="edit_review"), #PUT
    path("reviews/delete/<int:pk>/", api_show_review, name="delete_review"), #DELETE
]