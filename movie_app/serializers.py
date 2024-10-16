from rest_framework import serializers
from movie_app.models import Director, Movie, Review
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'name movie_count'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id title description duration director review_list rating '.split()


class DirectorValidationSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=5, max_length=100)


class MovieValidationSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=100)
    description = serializers.CharField(min_length=5)
    duration = serializers.IntegerField(min_value=1, max_value=10000)
    director_id = serializers.IntegerField()

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise serializers.ValidationError('Director does not exist')
        return director_id


class ReviewValidationSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=5, max_length=100)
    movie_id = serializers.IntegerField()
    stars = serializers.FloatField(max_value=5)

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except:
            raise serializers.ValidationError('Movie does not exist')
        return movie_id

    def validate_stars(self, stars):
        if stars < 0:
            raise serializers.ValidationError('Stars must be greater than or equal to 0')
        return stars
