from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from movie_app.serializers import (DirectorSerializer,
                                   MovieSerializer,
                                   ReviewSerializer,
                                   MovieReviewSerializer,
                                   DirectorValidationSerializer,
                                   MovieValidationSerializer,
                                   ReviewValidationSerializer,)
from movie_app.models import Director, Movie, Review


@api_view(['GET', 'POST'])
def directors_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.prefetch_related('movies').all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        serializer = DirectorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        director = Director.objects.create(
            **request.data
        )
        return Response(data={'director_id': director.id},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def directors_detail_api_view(request, id):
    try:
        directors = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"detail": "Director not found"}
        )

    if request.method == 'GET':
        data = DirectorSerializer(directors).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = DirectorValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        directors.name = serializer.validated_data.get('name')
        directors.save()
        return Response(data=DirectorSerializer(directors).data,
                        status=status.HTTP_201_CREATED)

    else:
        directors.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def movies_list_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieSerializer(movies, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        serializer = MovieValidationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        movie = Movie.objects.create(
            **request.data
        )
        return Response(data={'movie_id': movie.id},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"detail": "Director not found"}
        )

    if request.method == 'GET':
        data = MovieSerializer(movie).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = MovieValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
        movie.save()
        return Response(data=MovieSerializer(movie).data,
                        status=status.HTTP_201_CREATED)

    else:
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewSerializer(review, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        serializer = ReviewValidationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        review = Review.objects.create(
            **request.data
        )
        return Response(data={'review_id': review.id},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"detail": "Review not found"}
        )
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = ReviewValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)

        review.text = serializer.validated_data.get('text')
        review.movie_id = serializer.validated_data.get('movie_id')
        review.stars = serializer.validated_data.get('stars')
        review.save()

        return Response(data=ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)

    else:
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def review_movie_api_view(request):
    movies = Movie.objects.select_related('director').prefetch_related('reviews').all()
    data = MovieReviewSerializer(movies, many=True).data
    return Response(data=data)
