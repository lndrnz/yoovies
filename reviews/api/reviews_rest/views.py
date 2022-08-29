
# from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

import json


from common.json import ModelEncoder

from .models import Review, Movie, UserVO
# Create your views here.

class UserVOEncoder(ModelEncoder):
    model = UserVO
    properties = [
        "user_name"
    ]


class MovieEncoder(ModelEncoder):
    model = Movie
    properties = [
        "imdb_id",
        "title",
        # "year",
        # "rated",
        # "released",
        # "runtime",
        # "genre",
        # "director",
        # "writer",
        # "actors",
        # "plot"
    ]


class ReviewsEncoder(ModelEncoder):
    model = Review
    properties = ["title", "post", "rating","date", "movie", "user"]

    encoders = {"movie": MovieEncoder(), "user": UserVOEncoder()}


@require_http_methods(["GET"])
def api_list_movies(request):
    if request.method == "GET":

        movies = Movie.objects.all()
        return JsonResponse({"movies": movies}, encoder=MovieEncoder)


@require_http_methods(["GET"])
def api_list_reviews_by_imdb_id(request, imdb_id = None):
    if request.method == "GET":
        try:
            # content = json.loads(request.body)
            # imdb_id = content["imdb_id"]
            movie = Movie.objects.get(imdb_id=imdb_id)
            id = movie.id
        except Movie.DoesNotExist:
            return JsonResponse({"message": "movie does not exist in database"})
        reviews = Review.objects.filter(movie=id)
        return JsonResponse(reviews, ReviewsEncoder, safe=False)


@require_http_methods(["GET", "POST"])
def api_list_reviews(request, movie_id=None):
    if request.method == "GET":

        if movie_id != None:
            try:

                reviews = Review.objects.filter(movie=movie_id)

            except Movie.DoesNotExist:
                return JsonResponse(
                    {"message": "invalid movie id"}
                )
            return JsonResponse(
                reviews,
                encoder=ReviewsEncoder,
                safe=False
            )
        else: 
            return JsonResponse({"message": "please enter a movie id"})

    else:
        content = json.loads(request.body)
        try:
            movie = Movie.objects.get(id=movie_id)

        except Movie.DoesNotExist:
            return JsonResponse(
                {
                    "message": "invalid movie id",

                },
                status=400
            )
        content["movie"] = movie
        review = Review.objects.create(**content)
        return JsonResponse(
            review, encoder=ReviewsEncoder, safe=False
        )


@require_http_methods(["DELETE", "PUT"])
def api_show_review(request, pk):

    if request.method == "DELETE":
        count, _ = Review.objects.filter(id=pk).delete()
        return JsonResponse({"deleted": count > 0})

    else:  # PUT
        content = json.loads(request.body)

        try:
            if "movie" in content:
                movie = Movie.objects.get(id=content["movie"])
                content["movie"] = movie
        except Movie.DoesNotExist:
            return JsonResponse(
                {"message": "invalid movie"},
                status=400
            )

        Review.objects.filter(id=pk).update(**content)
        review = Review.objects.get(id=pk)
        return JsonResponse(
            review,
            encoder=ReviewsEncoder,
            safe=False,
        )
