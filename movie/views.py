from django.shortcuts import render
from django.http import JsonResponse
import os
from urllib.request import urlopen
import json
from movie.models import Movie, Comment
import time
from django.db.models import Count

def fetch_movie_data(title):
    url = "https://www.omdbapi.com/"
    parameters = "?apikey=" + os.environ['OMDb_API_Key'] + "&t=" + title

    # get movie info from omdb(put into function later)
    with urlopen(url + parameters) as url_responce:
        movie_data = json.loads(url_responce.read().decode('utf8'))

    return movie_data

def save_movie_data(movie_data):
    movie_data.pop('Response')
    new_movie_data = Movie(**movie_data)
    new_movie_data.save()


def movies(request, arg0='', arg1=''):
    if request.method == "POST":
        # check if title is given
        if arg0 == '':
            response = {"response":False, "error": "search title is missing"}
        else:
            movie_data = fetch_movie_data(arg0.replace(" ", "+"))

            # if title is found
            if movie_data['Response'] == "True":
                # if title is not in local db yet
                if not Movie.objects.filter(imdbID=movie_data['imdbID']).exists():
                    # save to db
                    save_movie_data(movie_data)

                response = {"response": True, "result": movie_data}

            # if title is not in omdb
            else:
                response = {"response":False, "error": "title is not found in OMDb"}

    elif request.method == "GET":
        if arg0 and arg1 == 'DESC' and Movie.model_field_exists(arg0):
            response = {"response": True, "result": list(Movie.objects.all().order_by("-" + arg0).values())}
        elif arg0 and Movie.model_field_exists(arg0)                                                                                  :
            response = {"response": True, "result": list(Movie.objects.all().order_by(arg0).values())}
        else:
            response = {"response": True, "result": list(Movie.objects.all().values())}

    return JsonResponse(response)


def comments(request, arg0='', arg1=''):
    if request.method == "POST":
        if not arg0 or not arg1:
            response = {"response":False, "error": "imdbID and comment are required"}
        elif not Movie.objects.filter(imdbID=arg0).exists():
            response = {"response":False, "error": "chosen imdbID doesn't exist in movie table"}
        else:
            new_comment = Comment(imdbID = arg0, comment = arg1.replace("+", " "), date = int(time.time()))
            new_comment.save()
            response = {"response": True, "result": {"imdbID": arg0, "comment": arg1}}

    elif request.method == "GET":
        if arg0 and not Comment.objects.filter(imdbID=arg0).exists():
            response = {"response": False, "error": "chosen imdbID doesn't exist in comment table"}
        elif arg0:
            response = {"response": True, "result": list(Comment.objects.filter(imdbID=arg0).values("imdbID", "comment"))}
        else:
            response = {"response": True, "result": list(Comment.objects.all().values("imdbID", "comment"))}

    return JsonResponse(response)


def top(request):
    if request.method == "GET":
        startdate = int(time.time()) - 60 * 60 * 24 * 31
        comments = Comment.objects.filter(date__gt=startdate).values('imdbID').annotate(total=Count('imdbID')).order_by('-total')
        rank = 1
        prevtotal = 0
        top_ten = []

        for i in comments:
            if i['total'] < prevtotal:
                rank +=1
            if rank > 10:
                break
            i['rank'] = rank
            top_ten.append(i)
            prevtotal = i['total']

        response = {"response": True, "results": top_ten}

    return JsonResponse(response)
