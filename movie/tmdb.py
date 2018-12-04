from django.conf import settings
import requests

class TMDB(object):

    def __init__(self):

        if settings.TMDB_API_KEY is '':
            raise Exception('No TMDB_API_KEY given')

        if settings.TMDB_BASE_URL is '':
            raise Exception('No TMDB_BASE_URL given')

        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
    
    def getMovieInfo(self, id, lang='pt-BR'):
        movie_info = None
        tmdb_request = requests.get('{}{}?api_key={}&language={}'.format(self.base_url, id, self.api_key, lang))

        if tmdb_request.status_code == 200:
            movie_info = tmdb_request.json()

        return movie_info
    
    def getMoviePopular(self, lang='pt-BR'):
        movies_result = None
        tmdb_request = requests.get('{}{}?api_key={}&language={}'.format(self.base_url, 'popular', self.api_key, lang))
        if tmdb_request.status_code == 200:
            movies_result = tmdb_request.json()

        return movies_result
    
    def getMovieRecommendation(self, id, lang='pt-BR'):
        movies_recommendations = None
        tmdb_request = requests.get('{}{}/{}?api_key={}&language={}'.format(self.base_url, id, 'recommendations', self.api_key, lang))
        if tmdb_request.status_code == 200:
            movies_recommendations = tmdb_request.json()

        return movies_recommendations

    def getMovieSimilar(self, id, lang='pt-BR'):
        movies_similar = None
        tmdb_request = requests.get('{}{}/{}?api_key={}&language={}'.format(self.base_url, id, 'similar', self.api_key, lang))
        if tmdb_request.status_code == 200:
            movies_similar = tmdb_request.json()

        return movies_similar
    
    def getMovieImage(self, backdrop_path):
        movie_image = None
        tmdb_request = requests.get('https://image.tmdb.org/t/p/w500{}'.format(backdrop_path))
        if tmdb_request.status_code == 200:
            movie_image = tmdb_request

        return movie_image

    def getMovieGenres(self, lang='pt-BR'):
        movies_genre = None
        tmdb_request = requests.get('http://api.themoviedb.org/3/genre/movie/list?api_key={}&language={}'.format(self.api_key, lang))
        if tmdb_request.status_code == 200:
            movies_genre = tmdb_request.json()

        return movies_genre
    
    def getMovieGenres(self, lang='pt-BR'):
        movies_genre = None
        tmdb_request = requests.get('http://api.themoviedb.org/3/genre/movie/list?api_key={}&language={}'.format(self.api_key, lang))
        if tmdb_request.status_code == 200:
            movies_genre = tmdb_request.json()

        return movies_genre
