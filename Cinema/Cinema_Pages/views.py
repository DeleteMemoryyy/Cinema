# -*- coding: UTF-8 -*-

from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views import View
from .func import fuzzy_finder
from .func import GetOtherInfo
from .models import Movie
from .models import Review
from .forms import ReviewForm
import MySQLdb


def index(request):
    return render(request, 'index.html')


def movie_display(request):
    try:
        movies_list = Movie.objects.order_by('-year')  # 降序
        paginator = Paginator(movies_list, 30)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        return render(request, 'movie_display.html', {'movies': movies})
    except:
        return render(request, '404.html')


def movie_detail(request, id):
    try:
        movie = Movie.objects.get(id=id)
        # if request.method == 'GET':
        #     conn = MySQLdb.connect(
        #         host='localhost',
        #         port=3306,
        #         user='root',
        #         passwd='xt032341',
        #         db='cinema'
        #     )
        #     cursor = conn.cursor()
        #     sqlstr = 'SELECT * FROM Cinema_Pages_movie WHERE id = {0}'.format(id)
        #     print(sqlstr)
        #     cursor.execute(sqlstr)
        #     values = cursor.fetchall()
        #     print(values)
        datas = Movie.objects.all()
        recommend_list = []
        for data in datas:
            if movie.genres.split(',')[0] in data.genres:
                recommend_list.append(data)
        recommend_list.remove(movie)  # 去除重复项
        other_info = GetOtherInfo(id)

        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='xt032341',
            db='cinema',
            use_unicode=True,
            charset="utf8"
        )
        cursor = conn.cursor()
        sql_str = 'SELECT * FROM Cinema_Pages_review WHERE movie_id_id = {0}'.format(id)
        print(sql_str)
        cursor.execute(sql_str)
        reviews_raw = cursor.fetchall()
        review_list = []
        for review_r in reviews_raw:
            review_list.append(Review(review_r))

        form = ReviewForm()

        context = {'movie': movie, 'recommend_list': recommend_list[:12], 'other_info': other_info,
                   'review_list': review_list, 'form': form}
        return render(request, 'movie_detail.html', context)
    except (KeyError, ValueError):
        return render(request, '404.html')
        # pass


def add_review(request, movie_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.clean()
            author = form.cleaned_data['author']
            score = form.cleaned_data['score']
            content = form.cleaned_data['content']

            sql_str = "INSERT INTO Cinema_Pages_review VALUES (NULL, {movie_id}, {score}, NULL, \'{author}\', \'{content}\')".format(
                movie_id=movie_id, score=score, author=author, content=content)

            conn = MySQLdb.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='xt032341',
                db='cinema',
                # use_unicode=True,
                charset="utf8"
            )
            cursor = conn.cursor()
            cursor.execute(sql_str)
            print(sql_str)

            conn.commit()

            cursor.close()
            conn.close()

    return redirect('../')

def movie_search_by_genre(request, genre):
    try:
        datas = Movie.objects.all()
        movies_list = []
        for data in datas:
            if genre in data.genres:
                movies_list.append(data)

        paginator = Paginator(movies_list, 12)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        context = {'movies': movies}
        return render(request, 'movie_display.html', context)
    except:
        return render(request, '404.html')


def movie_search_by_year(request, year):
    # 使用Movie.objects.filter(year = year)更佳
    try:
        movies_list = []
        datas = Movie.objects.all()
        for data in datas:
            if str(year) == data.year:
                movies_list.append(data)
            else:
                if str(year) == data.year[:2]:
                    movies_list.append(data)

        paginator = Paginator(movies_list, 12)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        context = {'movies': movies}
        return render(request, 'movie_display.html', context)
    except:
        return render(request, '404.html')


# def movie_search_form(request):
#     非模糊查询
#     title = request.POST.get('q')
#     movies_list = Movie.objects.filter(title=title)
#     paginator = Paginator(movies_list, 4)
#     page = request.GET.get('page')
#     movies = paginator.get_page(page)
#     return render(request, 'index.html', {'movies': movies})


def movie_search_form(request):
    # 模糊查询
    try:
        q = request.POST.get('q')
        collection = Movie.objects.all()
        movies_list = fuzzy_finder(q, collection)
        paginator = Paginator(movies_list, 30)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        return render(request, 'movie_display.html', {'movies': movies})
    except:
        return render(request, '404.html')


# API


def search_by_id(request, id):
    try:
        data = model_to_dict(Movie.objects.get(id=id))
    except:
        raise Http404("Movie does not exist.")
    return JsonResponse(data, safe=False)


# a new api for reference
# def searchbyid(request):
#     try:
#         id = request.GET.get('id')
#         data = model_to_dict(Movie.objects.get(id=id))
#     except:
#         raise Http404("Movie does not exist.")
#     return JsonResponse(data, safe=False)


def search_by_title(request, title):
    try:
        data = model_to_dict(Movie.objects.get(title=title))
        return JsonResponse(data, safe=False)
    except:
        raise Http404("Movie does not exist.")


def search_by_original_title(request, original_title):
    try:
        data = model_to_dict(Movie.objects.get(original_title=original_title))
        return JsonResponse(data, safe=False)
    except:
        raise Http404("Movie does not exist.")


def search_by_genre(request, genre):
    try:
        data = list(Movie.objects.all())
        find = []
        json = {}
        for d in data:
            if genre in model_to_dict(d)['genres']:
                find.append(model_to_dict(d))
        json['subject'] = find
        return JsonResponse(json, safe=False)
    except:
        raise Http404("Movie does not exist.")


def search_by_year(request, year):
    try:
        data = list(Movie.objects.all())
        find = []
        json = {}
        for d in data:
            if year == model_to_dict(d)['year']:
                find.append(model_to_dict(d))
        json['subject'] = find
        return JsonResponse(json, safe=False)
    except:
        raise Http404("Movie does not exist.")
