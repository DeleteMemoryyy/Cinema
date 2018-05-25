from django.shortcuts import render
from .models import Movie, MyMovie
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .func import fuzzy_finder
from .func import GetOtherInfo
import MySQLdb


def index(request):
    return render(request, 'index.html')


def movie_display(request):
    try:
        db = MySQLdb.connect('localhost', 'root', 'mysql9772', 'mycinema',use_unicode=True, charset="utf8")
        cur = db.cursor()
        sqlquery = 'select * from fullmovie order by M_releaseDate desc;'
        res_ = cur.execute(sqlquery)
        res = cur.fetchmany(res_)

    
        movies_list = []
        
        start_id, title, image = res[0][0], res[0][2], res[0][5]
        rating= res[0][7]
        movies_list.append(MyMovie(start_id, 'a', title, 'a', 'a', image, 'a', 'NULL', rating, 'a', 'a', 'a'))
        for mv in res:
            if mv[0] != start_id:
                start_id, title,image = mv[0], mv[2],  mv[5];
                rating= mv[7]
                tmp = MyMovie(start_id, 'alt', title, 'ori_title', 'year', image, 'genres', 'NULL', \
                    rating, 'directors', 'casts', 'intro')
                movies_list.append(tmp)
        #movies_list = Movie.objects.order_by('-year')  # 降序
        
        paginator = Paginator(movies_list, 30)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        return render(request, 'movie_display.html', {'movies': movies})
    except:
        return render(request, '404.html')


def movie_detail(request, id):
    try:
        '''
        movie = Movie.objects.get(id=id)
        print(movie)
        datas = Movie.objects.all()
        recommend_list = []
        for data in datas:
            if movie.genres.split(',')[0] in data.genres:
                recommend_list.append(data)
        recommend_list.remove(movie)  # 去除重复项
        '''
        
        db = MySQLdb.connect('localhost', 'root', 'mysql9772', 'mycinema',use_unicode=True, charset="utf8")
        cur = db.cursor()
        sqlquery = 'select * from fullmovie where M_id ='  + str(id) + ';'
        res_ = cur.execute(sqlquery)
        res = cur.fetchmany(res_)
        
        #print(res)
        
        start_id,alt, title, ori_title = res[0][0], res[0][1], res[0][2], res[0][3]
        year, image = res[0][4], res[0][5]
        d_list, a_list, g_list = [], [], []
        gener = res[0][-5]
        rating = res[0][7]
        for mv in res:
            if mv[-3] not in d_list:
                d_list.append(mv[-3])

            if mv[-2] not in a_list:
                a_list.append(mv[-2])

            if mv[-5] not in g_list:
                g_list.append(mv[-5])
                
        directors = d_list[0]
        for i in range(1, len(d_list)):
            directors += ',' + d_list[i]

        casts = a_list[0]
        for i in range(1, len(a_list)):
            casts += ',' + a_list[i]

        genres = g_list[0]
        for i in range(1, len(g_list)):
            genres += ',' + g_list[i]

        print(directors)
        print(casts)
        print(genres)
        movie = MyMovie(start_id, alt, title, ori_title, year, image, genres, 'NULL', \
            rating, directors, casts, 'intro')

        print(gener)
        genresearchsql = 'select * from fullmovie where c_name = \'' + gener +'\';'
        recommend_res_ = cur.execute(genresearchsql)
        reommend_res = cur.fetchmany(recommend_res_)
        recommend_list = []
        start_id, title, image = reommend_res[0][0], reommend_res[0][2], reommend_res[0][5]
        rating= reommend_res[0][7]
        recommend_list.append(MyMovie(start_id, 'a', title, 'a', 'a', image, 'a', 'NULL', rating, 'a', 'a', 'a'))
        for mv in reommend_res:
            if mv[0] != start_id:
                start_id, title,image = mv[0], mv[2],  mv[5];
                rating= mv[7]
                tmp = MyMovie(start_id, 'alt', title, 'ori_title', 'year', image, 'genres', 'NULL', \
                    rating, 'directors', 'casts', 'intro')
                recommend_list.append(tmp)
            
    
        other_info = GetOtherInfo(id)
        context = {'movie': movie, 'recommend_list': recommend_list, 'other_info': other_info}
        return render(request, 'movie_detail.html', context)
    except (KeyError, ValueError):
        return render(request, '404.html')
        # pass


def movie_search_by_genre(request, genre):
    try:
        '''
        datas = Movie.objects.all()
        movies_list = []
        for data in datas:
        if genre in data.genres:
        movies_list.append(data)
        '''
        db = MySQLdb.connect('localhost', 'root', 'mysql9772', 'mycinema',use_unicode=True, charset="utf8")
        cur = db.cursor()
        sqlquery = 'select * from fullmovie where C_name = \'' + str(genre) + '\';'
        res_ = cur.execute(sqlquery)
        res = cur.fetchmany(res_)

    
        movies_list = []
        
        start_id, title, image = res[0][0], res[0][2], res[0][5]
        rating= res[0][7]
        movies_list.append(MyMovie(start_id, 'a', title, 'a', 'a', image, 'a', 'NULL', rating, 'a', 'a', 'a'))
        for mv in res:
            if mv[0] != start_id:
                start_id, title,image = mv[0], mv[2],  mv[5];
                rating= mv[7]
                tmp = MyMovie(start_id, 'alt', title, 'ori_title', 'year', image, 'genres', 'NULL', \
                    rating, 'directors', 'casts', 'intro')
                movies_list.append(tmp)
    
        #print(movies_list)
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
        db = MySQLdb.connect('localhost', 'root', 'mysql9772', 'mycinema',use_unicode=True, charset="utf8")
        cur = db.cursor()
        sqlquery = 'select * from fullmovie where M_releaseDate = \'' + str(year) + '\';'
        res_ = cur.execute(sqlquery)
        res = cur.fetchmany(res_)
  
        movies_list = []
        
        start_id, title, image = res[0][0], res[0][2], res[0][5]
        rating= res[0][7]
        movies_list.append(MyMovie(start_id, 'a', title, 'a', 'a', image, 'a', 'NULL', rating, 'a', 'a', 'a'))
        for mv in res:
            if mv[0] != start_id:
                start_id, title,image = mv[0], mv[2],  mv[5];
                rating= mv[7]
                tmp = MyMovie(start_id, 'alt', title, 'ori_title', 'year', image, 'genres', 'NULL', \
                    rating, 'directors', 'casts', 'intro')
                movies_list.append(tmp)

        # datas = Movie.objects.all()
        # movies_list = []
        # for data in datas:
        #     if str(year) == data.year:
        #         print(data)
        #         movies_list.append(data)
        #     else:
        #         if str(year) == data.year[:2]:
        #             movies_list.append(data)

       
        paginator = Paginator(movies_list, 12)
 
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        context = {'movies': movies}
        return render(request, 'movie_display.html', context)
    except:
        print('render gots an error!')
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
        #collection = Movie.objects.all()
        collection = []
        
        db = MySQLdb.connect('localhost', 'root', 'mysql9772', 'mycinema',use_unicode=True, charset="utf8")
        cur = db.cursor()
        sqlquery = 'select * from fullmovie;'
        res_ = cur.execute(sqlquery)
        res = cur.fetchmany(res_)
        
        start_id, title, image = res[0][0], res[0][2], res[0][5]
        rating= res[0][7]
        collection.append(MyMovie(start_id, 'a', title, 'a', 'a', image, 'a', 'NULL', rating, 'a', 'a', 'a'))
        for mv in res:
            if mv[0] != start_id:
                start_id, title,image = mv[0], mv[2],  mv[5];
                rating= mv[7]
                tmp = MyMovie(start_id, 'alt', title, 'ori_title', 'year', image, 'genres', 'NULL', \
                    rating, 'directors', 'casts', 'intro')
                collection.append(tmp)
        
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
