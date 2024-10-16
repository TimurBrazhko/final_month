from django.urls import path
from movie_app.views import (directors_list_create_api_view, directors_detail_api_view,
                             movies_list_api_view, movie_detail_api_view,
                             review_list_create_api_view, review_detail_api_view)

app_name = 'movie_app'

urlpatterns = [
    path('directors/', directors_list_create_api_view, name='directors_list_create'),
    path('directors/<int:id>/', directors_detail_api_view, name='directors_detail'),
    path('movie/', movies_list_api_view, name='movies_list'),
    path('movie/<int:id>/', movie_detail_api_view, name='movie_detail'),
    path('review/', review_list_create_api_view, name='review_list_create'),
    path('review/<int:id>/', review_detail_api_view, name='review_detail'),
]