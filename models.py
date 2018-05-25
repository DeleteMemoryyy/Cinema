from django.db import models

# Create your models here.


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    alt = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    original_title = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=10)
    image = models.CharField(max_length=255, null=True, blank=True)
    genres = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    directors = models.CharField(max_length=100, null=True, blank=True)
    casts = models.CharField(max_length=100, null=True, blank=True)
    intro = models.TextField(null=True, blank=True)


    # def __init__(self, _id, _alt, _title, _orititle, _year, _image, _gen, _reg, _rat, _dir, _cast, _intro):
    #     super(Movie, self).__init__()
    #     id = _id
    #     alt = _alt
    #     title, original_title = _title, _orititle
    #     year, image, genres = _year, _image, _gen
    #     region, rating = _reg, _rat
    #     directors = _dir
    #     casts = _cast
    #     intro = _intro

    # 添加以下代码，在网站后台访问会报错
    # def __str__(self):
    #     return self.intro[:20] + '...'


class MyMovie():
    def __init__(self, _id, _alt, _title, _orginal_title, _year, _image, _genres, _region, _rating, _directors, _casts, _intro):
        self.id = _id
        self.alt = _alt
        self.title = _title
        self.original_title = _orginal_title
        self.year = _year
        self.image = _image
        self.genres = _genres
        self.region = _region
        self.rating = _rating
        self.directors = _directors
        self.casts = _casts
        self.intro  = _intro
    

if __name__ == 'main':
    Movie(1,'2','3','4','5','6','7','8',1.2,'asdf', 'asdfads','asdfasdf')