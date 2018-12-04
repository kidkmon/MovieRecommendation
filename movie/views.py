from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from .tmdb import TMDB
from math import sqrt
from django.conf import settings
import requests

def post_list(request):
    tmdb = TMDB()
    movies = tmdb.getMoviePopular()
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'movie/post_list.html', {'movies': movies['results']})

def post_detail(request, pk):
    tmdb = TMDB()
    movie = tmdb.getMovieInfo(id=pk)
    movies_recommended = tmdb.getMovieSimilar(id=pk)
    
    if(movies_recommended['results'] == []):
        movies_recommended = tmdb.getMovieRecommendation(id=pk)['results']
    else:
        movies_recommended = sorted(movies_recommended['results'], key=lambda k: k.get('vote_average'), reverse=True)

    return render(request, 'movie/post_detail.html', {'movie': movie, 'movies_recommended': movies_recommended[:5]})

def genre(request):
    tmdb = TMDB()
    movies_genre = tmdb.getMovieGenres()['genres']
    return render(request, 'movie/post_edit.html', {'genres': movies_genre})

def post_new(request):
     if request.method == "POST":
         form = PostForm(request.POST)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.published_date = timezone.now()
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm()
     return render(request, 'movie/post_edit.html', {'form': form})

def post_edit(request, pk):
     post = get_object_or_404(Post, pk=pk)
     if request.method == "POST":
         form = PostForm(request.POST, instance=post)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.published_date = timezone.now()
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm(instance=post)
     return render(request, 'movie/post_edit.html', {'form': form})

def euclidian(vector1, vector2):
    distance = 0
    for i in range(len(vector1)):
        distance += pow((vector1[i]-vector2[i]), 2)
    total = sqrt(distance)
    return total

def compute_nearest_neighbor(item_name, item_vector, items):
    distances = []
    for other_item in items:
        if(other_item != item_name):
            distance = euclidian(item_vector, items[other_item])
            distances.append((distance, other_item))
    distances.sort()
    return distances

def classify(movie, item_name, item_vector):
    nearest = compute_nearest_neighbor(movie, item_name, item_vector)[0][:5]
    return nearest


def getMovieRecommendation(id,  movie_name, movies, lang='pt-BR'):
    movies_recommendations = compute_nearest_neighbor(movie_name, movies[id] ,movies)
    movies_recommendations_json = []
    for movie in movies_recommendations:
        tmdb_request = requests.get('{}{}?api_key={}&language={}'.format(self.base_url, id, self.api_key, lang))    
        if tmdb_request.status_code == 200:
            movies_recommendations_json.append(tmdb_request.json())

    return movies_recommendations_json
