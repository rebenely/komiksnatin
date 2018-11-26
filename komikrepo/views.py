from django.shortcuts import render, redirect
from django.http import HttpResponse
from komikrepo.forms import *
from komikrepo.models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.db import connection
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
import json


def index(request):
    komik = Komik.objects.all().order_by('-rating')[:5]
    context = {'hello': 'Test', 'komiks': komik}
    return render(request, 'komikrepo/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.account.description = form.cleaned_data.get('description')
            user.account.account_type = 'basic';
            user.save()
            print (connection.queries)

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def accountView(request, username):
    result = Account.objects.get(username=username)
    review = Review.objects.filter(user=result)
    context = {'account': result.username, 'description': result.description, 'reviews' : review }
    return render(request, 'komikrepo/account.html', context)

def deleteAccount(request, username):
    deleted = False
    if request.method == 'POST':
        print(request.POST)
        if request.user.is_authenticated and request.user.username == username and request.POST['password']:
            u = authenticate(username=username, password=request.POST['password'])
            if u:
                u.delete()
                deleted = True
                logout(request)

    context = {'success': deleted}
    return render(request, 'registration/delete.html', context)

def editAccount(request, username):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if request.user.is_authenticated and request.user.username == username:
            print(request.POST)
            if form.is_valid():
                print('reached here')
                user = User.objects.get(username=username)
                user.account.description = form.cleaned_data.get('description')
                user.account.account_type = 'basic';
                raw_password = form.cleaned_data.get('password1')
                user.set_password(raw_password)
                print('password ',raw_password )
                login(request, user)
                user.save()
                return redirect('/account/'+username)
    else:
        form = EditForm()
        if request.user.username != username:
            raise PermissionDenied
    return render(request, 'registration/edit.html', {'form': form})

def listKomiks(request, page=1):
    if request.method == 'GET':
        if request.GET:
            print(request.GET)
            if(request.GET.get('search')):
                komik_list = Komik.objects.filter(title__icontains=request.GET.get('search')).order_by('-rating')
            else:
                komik_list = Komik.objects.all().order_by('-rating')
            for entry in request.GET:
                print(entry)

                if entry != 'search' and entry != 'sort':
                    komik_list = komik_list.filter(komik_tags=Tag.objects.filter(name=entry)[0])
                    print(komik_list)
                if entry == 'sort':
                    order = request.GET.get('sort', '')
                    if order == 'abc':
                        komik_list = komik_list.order_by('title')
                    elif order == 'cba':
                        komik_list = komik_list.order_by('-title')
                    elif order == 'rating':
                        # default behavior
                        komik_list = komik_list.order_by('-rating')
                    elif order == 'gnitar':
                        komik_list = komik_list.order_by('rating')


        else:
            komik_list = Komik.objects.all().order_by('-rating')

        paginator = Paginator(komik_list, 10)
        print('page no is', page)
        try:
            komiks = paginator.page(page)
        except PageNotAnInteger:
            komiks = paginator.page(1)
        except EmptyPage:
            komiks = paginator.page(paginator.num_pages)
        context = {'hello': 'post'}
    else:
        komiks = Komik.objects.all()
    return render(request, 'komikrepo/komikslist.html', {'komiks': komiks, 'querySet': request.GET.urlencode()})

def viewKomik(request, id):
    try:
        komik = Komik.objects.get(id=id)
        reviews = Review.objects.filter(komik=komik)
        user = Account.objects.get(username=request.user.username)
        try:
            reviews.get(user=user)
            canAdd = False
        except Review.DoesNotExist:
            canAdd = True
        print(komik)
    except Komik.DoesNotExist:
        raise Http404("Komik does not exist")
    except Account.DoesNotExist:
        canAdd = False
    return render(request, 'komikrepo/komikview.html', {'komik': komik, 'reviews': reviews, 'canAdd': canAdd })

def reviewKomik(request, id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            print('found one ' + str(form.cleaned_data.get('rating')))
            try:
                komik = Komik.objects.get(id=id)
                user = Account.objects.get(username=request.user.username)
                rating = form.cleaned_data.get('rating')
                comment = form.cleaned_data.get('comment')
                r = Review(user=user, komik=komik, rating=rating, comment=comment)
                r.save()
                print(komik)
            except Komik.DoesNotExist:
                raise Http404("Komik does not exist")
    else:
        form = ReviewForm()
        return render(request, 'komikrepo/reviewkomik.html', {'form': form})
    return redirect('/komik/'+str(id))

def editReviewKomik(request, id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            print('found one ' + str(form.cleaned_data.get('rating')))
            try:
                komik = Komik.objects.get(id=id)
                user = Account.objects.get(username=request.user.username)
                old_review = Review.objects.get(komik=komik, user=user)

                rating = form.cleaned_data.get('rating')
                comment = form.cleaned_data.get('comment')
                old_review.rating = rating;
                old_review.comment = comment;
                old_review.save()
            except Komik.DoesNotExist or Account.DoesNotExist or Review.DoesNotExist:
                raise Http404("Error retreiving from DB")
    else:
        form = ReviewForm()
        try:
            komik = Komik.objects.get(id=id)
            user = Account.objects.get(username=request.user.username)
            review = Review.objects.get(komik=komik, user=user)
        except Komik.DoesNotExist or Account.DoesNotExist or Review.DoesNotExist:
            raise Http404("Error retreiving from DB")

        return render(request, 'komikrepo/reviewkomik.html', {'form': form, 'review': review})
    return redirect('/komik/'+str(id))

def deleteReviewKomik(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                komik = Komik.objects.get(id=id)
                user = Account.objects.get(username=request.user.username)
                old_review = Review.objects.get(komik=komik, user=user)
                old_review.delete()
            except Komik.DoesNotExist or Account.DoesNotExist or Review.DoesNotExist:
                raise Http404("Error retreiving from DB")
    else:
        return redirect('/komik/'+str(id))
    return redirect('/komik/'+str(id))

def updateList(request, id):
    if request.method == 'POST':
        return redirect('/')
    else:
        if request.user.is_authenticated:
            try:
                user = Account.objects.get(username=request.user.username)
                list = List.objects.get(id=id, user=user)
            except List.DoesNotExist:
                raise Http404("List does not exist!")
        return render(request, 'komikrepo/list.html', {'id': list.id, 'title': list.title})
    return render(request, 'komikrepo/list.html')

def createList(request):
    if request.method == 'POST':
        form = ListCreateForm(request.POST)
        print(form.is_valid())
        if form.is_valid() and request.user.is_authenticated:
            print('found one ' + str(form.cleaned_data.get('title')))
            try:
                user = Account.objects.get(username=request.user.username)
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')

                l = List(user=user, title=title, description=description, list_size=0)
                l.save()
                print('crea sted!')
            except Account.DoesNotExist:
                raise Http404("Account does not exist!")
            return redirect('/list/edit/'+str(l.id))
        else:
            return redirect('/')

    else:
        form = ListCreateForm()
        return render(request, 'komikrepo/createlist.html', {'form': form})
    return render(request, 'komikrepo/list.html')

def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        komik_list = Komik.objects.filter(title__icontains=q).order_by('title')
        results = []
        print (q)
        for r in komik_list:
            temp = {}
            temp['label'] = r.title
            temp['value'] = r.id
            results.append(temp)
        data = json.dumps(results)
        print(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def getList(request):
    if request.user.is_authenticated and request.is_ajax():
        user = Account.objects.get(username=request.user.username)
        list = List.objects.get(user=user, id=request.GET.get('id', None))
        results = []
        sorted = ListRank.objects.filter(list=list).order_by('ranking')
        print(sorted)

        for item in sorted:
            komik = item.komik
            temp = {}
            temp['label'] = komik.title
            temp['value'] = komik.id
            temp['img'] = komik.image_url
            temp['desc'] = item.description
            results.append(temp)

        # for komik in list.list_komiks.all():
        #     temp = {}
        #     temp['label'] = komik.title
        #     temp['value'] = komik.id
        #     temp['img'] = komik.image_url
        #     results.append(temp)


        data = json.dumps(results)
        print(results)
    else:
        data = 'fail'
    return HttpResponse(data)


def addToList(request):
    print ('dafuq')
    if request.user.is_authenticated and request.is_ajax():
        print('pass')
        try:
            user = Account.objects.get(username=request.user.username)
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            komik = Komik.objects.get(id=request.POST.get('komik_id', None))
            listrank = ListRank(list=list, komik=komik,  ranking=request.POST.get('ranking', 1), description="test")
            listrank.save()
            data = {'label' : komik.title, 'value': komik.id, 'img': komik.image_url}
            data = json.dumps(data);
        except Account.DoesNotExist or List.DoesNotExist or Komik.DoesNotExist or IntegrityError:
            data = {'result' : 'fail'}
            data = json.dumps(data);
    else:
        data = {'result' : 'fail'}
        data = json.dumps(data);
    return HttpResponse(data)

def deleteFromList(request):
    print ('dafuq')
    if request.user.is_authenticated and request.is_ajax():
        print('pass')
        try:
            user = Account.objects.get(username=request.user.username)
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            komik = Komik.objects.get(id=request.POST.get('komik_id', None))
            listrank = ListRank.objects.get(komik=komik, list=list)
            rank = listrank.ranking
            listrank.delete()
            offsetRanks = ListRank.objects.filter(list=list, ranking__gt=rank).order_by('ranking');
            print(offsetRanks)
            for komik in offsetRanks:
                komik.ranking -= 1
                komik.save()

            data = {'result' : 'success'}
            data = json.dumps(data);
        except Account.DoesNotExist or List.DoesNotExist or Komik.DoesNotExist:
            data = {'result' : 'fail'}
            data = json.dumps(data);
    else:
        data = {'result' : 'fail'}
        data = json.dumps(data);
    return HttpResponse(data)

def sortList(request):
    if request.user.is_authenticated and request.is_ajax():
        print('pass')
        try:
            user = Account.objects.get(username=request.user.username)
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            sorted = json.loads(request.POST.get('komik_sort', None))
            print(sorted)
            for index, id in enumerate(sorted, start=1):
                komik = Komik.objects.get(id=id)
                listrank = ListRank.objects.get(komik=komik, list=list)
                listrank1 = ListRank.objects.get(list=list, ranking=index)
                temp = listrank.ranking
                listrank.ranking *= -1
                listrank.save()
                listrank1.ranking = temp
                listrank1.save()
                listrank.ranking = index
                listrank.save()

            data = {'result' : 'success'}
            data = json.dumps(data);
        except Account.DoesNotExist or List.DoesNotExist or Komik.DoesNotExist or ListRank.DoesNotExist:
            data = {'result' : 'fail'}
            data = json.dumps(data);
    else:
        data = {'result' : 'fail'}
        data = json.dumps(data);
    return HttpResponse(data)

def updateDesc(request):
    print ('dafuq')
    if request.user.is_authenticated and request.is_ajax():
        print('pass')
        try:
            user = Account.objects.get(username=request.user.username)
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            komik = Komik.objects.get(id=request.POST.get('komik_id', None))
            listrank = ListRank.objects.get(komik=komik, list=list)
            listrank.description = request.POST.get('description', '')
            listrank.save()
            data = {'result' : 'success'}
            data = json.dumps(data);
        except Account.DoesNotExist or List.DoesNotExist or Komik.DoesNotExist:
            data = {'result' : 'fail'}
            data = json.dumps(data);
    else:
        data = {'result' : 'fail'}
        data = json.dumps(data);
    return HttpResponse(data)



def listList(request, page=1):
    if request.method == 'GET':
        if request.GET:
            print(request.GET)
            if(request.GET.get('search')):
                list_list = List.objects.filter(title__icontains=request.GET.get('search')).order_by('title')
            else:
                list_list = List.objects.all().order_by('title')

        else:
            list_list = List.objects.all().order_by('title')

        paginator = Paginator(list_list, 10)
        print('page no is', page)
        try:
            lists = paginator.page(page)
        except PageNotAnInteger:
            lists = paginator.page(1)
        except EmptyPage:
            lists = paginator.page(paginator.num_pages)
        context = {'hello': 'post'}
    else:
        komiks = Komik.objects.all()
    return render(request, 'komikrepo/listlist.html', {'lists': lists, 'querySet': request.GET.urlencode()})

def viewList(request, id):
    try:
        list = List.objects.get(id=id)
        listrank = ListRank.objects.filter(list=list).order_by('ranking')
    except List.DoesNotExist:
        raise Http404("Komik does not exist")
    if request.user.is_authenticated and request.user.username == list.user:
        canAdd = True
    else:
        canAdd = False
    return render(request, 'komikrepo/listview.html', {'list': list, 'listrank': listrank, 'canAdd': canAdd })
