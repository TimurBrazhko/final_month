from django.contrib import admin
from movie_app.models import Movie, Director, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Director)
