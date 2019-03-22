from django.db import models


class Movie(models.Model):
    Title = models.CharField(max_length = 100)
    Year = models.CharField(max_length = 10)
    Rated = models.CharField(max_length = 10)
    Released = models.CharField(max_length = 15)
    Runtime = models.CharField(max_length = 10)
    Genre = models.CharField(max_length = 100)
    Director = models.CharField(max_length = 100)
    Writer = models.CharField(max_length = 100)
    Actors = models.CharField(max_length = 200)
    Plot = models.CharField(max_length = 500)
    Language = models.CharField(max_length = 100)
    Country = models.CharField(max_length = 50)
    Awards = models.CharField(max_length = 20)
    Poster = models.CharField(max_length = 250)
    Ratings = models.CharField(max_length = 500)
    Metascore = models.CharField(max_length = 5)
    imdbRating = models.CharField(max_length = 5)
    imdbVotes = models.CharField(max_length = 10)
    imdbID = models.CharField(max_length = 20, unique=True)
    Type = models.CharField(max_length = 10)
    TotalSeasons = models.CharField(max_length = 5)
    DVD = models.CharField(max_length = 15)
    BoxOffice = models.CharField(max_length = 15)
    Production = models.CharField(max_length = 50)
    Website = models.CharField(max_length = 250)

    @classmethod
    def model_field_exists(cls, field):
        try:
            cls._meta.get_field(field)
            return True
        except models.FieldDoesNotExist:
            return False


class Comment(models.Model):
    imdbID = models.CharField(max_length = 20)
    comment = models.CharField(max_length = 500)
    date = models.IntegerField()
