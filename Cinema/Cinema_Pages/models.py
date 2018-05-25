class Review():
    review_id = ''
    movie_id = ''
    score = ''
    time = ''
    author = ''
    content = ''

    def __init__(self, raw):
        if len(raw) == 6:
            self.review_id = raw[0]
            self.movie_id = raw[1]
            self.score = raw[2]
            self.time = raw[3]
            self.author = raw[4]
            self.content = raw[5]


class Movie():
    def __init__(self, _id, _alt, _title, _orginal_title, _year, _image, _genres, _region, _rating, _directors, _casts,
                 _intro, _viewnumber):
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
        self.intro = _intro
        self.viewnumber = _viewnumber
