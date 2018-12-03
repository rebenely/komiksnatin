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
from random import randint
import json


def index(request):
    # select * from komik order by rating desc, title asc limit 5;
    komik = Komik.objects.all().order_by('-rating', 'title')[:5]

    # select count(*) from list;
    num = List.objects.all().count()
    num = randint(0, num - 1)
    print(num)

    # this is equivalent to getting one row only but i did not use id=num because the num may be offset by previous ids
    # select * from list order by random() limit 1; I was told this was slow.
    randomList = List.objects.all()[num]
    context = {'hello': 'Test', 'komiks': komik, 'list': randomList}
    return render(request, 'komikrepo/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.account.description = form.cleaned_data.get('description')
            user.account.account_type = 'basic';

            # insert into auth_user (username, password) values (form.username, form.password);
            # this also triggers a django action which will create a profile (Account) row for this user
            # insert into account (username, description, accountType) values (form.username, form.description, 'basic');
            user.save()

            raw_password = form.cleaned_data.get('password1')
            # log user in
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def accountView(request, username):
    # select * from account where username=username;
    result = Account.objects.get(username=username)
    # select * from review where user=result order by rating desc;
    review = Review.objects.filter(user=result).order_by('-rating')
    # select * from list where user=result order by created desc;
    list = List.objects.filter(user=result).order_by('-created')
    context = {'account': result.username, 'description': result.description, 'reviews' : review, 'list': list }
    return render(request, 'komikrepo/account.html', context)

def deleteAccount(request, username):
    deleted = False
    if request.method == 'POST':
        print(request.POST)
        if request.user.is_authenticated and request.user.username == username and request.POST['password']:
            u = authenticate(username=username, password=request.POST['password'])
            if u:
                # delete from auth_user where username=username;
                # delete cascades
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
                if form.cleaned_data.get('password1'):
                    raw_password = form.cleaned_data.get('password1')
                    user.set_password(raw_password)
                    print('password ',raw_password )
                    login(request, user)
                user.save()
                # update auth_user set password=hashed(raw_password) where username=username;
                # update account set description=form.description where username=username;
                return redirect('/account/'+username)
    else:
        form = EditForm()
        if request.user.username != username:
            raise PermissionDenied
    return render(request, 'registration/edit.html', {'form': form})

def listKomiks(request, page=1):
    if request.method == 'GET':
        if request.GET:
            if(request.GET.get('search')):
                # select * from komik where title like '%form.search%' order by rating desc;
                komik_list = Komik.objects.filter(title__icontains=request.GET.get('search')).order_by('-rating')
            else:
                # select * from komik order by rating desc;
                komik_list = Komik.objects.all().order_by('-rating')
            for entry in request.GET:

                # these change the order but does not query the database anymore
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
            # select * from komik order by rating desc;
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
        # select * from komik where id=id;
        komik = Komik.objects.get(id=id)
        # select * from review order by rating desc;
        reviews = Review.objects.filter(komik=komik).order_by('-rating')
        # select * from account where username=request.user.username
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
                # select * from komik where id=id;
                komik = Komik.objects.get(id=id)
                # select * from account where username=request.user.username
                user = Account.objects.get(username=request.user.username)

                rating = form.cleaned_data.get('rating')
                comment = form.cleaned_data.get('comment')
                r = Review(user=user, komik=komik, rating=rating, comment=comment)
                # insert into review (rating, comment, komik_id, user_id) values (rating, comment, komik.id, comment);
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
                # select * from komik where id=id;
                komik = Komik.objects.get(id=id)
                # select * from account where username=request.user.username
                user = Account.objects.get(username=request.user.username)

                # select * from review where komik=komik, user=user
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
            # select * from komik where id=id;
            komik = Komik.objects.get(id=id)
            # select * from account where username=request.user.username
            user = Account.objects.get(username=request.user.username)
            # select * from review where komik=komik, user=user
            review = Review.objects.get(komik=komik, user=user)
        except Komik.DoesNotExist or Account.DoesNotExist or Review.DoesNotExist:
            raise Http404("Error retreiving from DB")

        return render(request, 'komikrepo/reviewkomik.html', {'form': form, 'review': review})
    return redirect('/komik/'+str(id))

def deleteReviewKomik(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                # select * from komik where id=id;
                komik = Komik.objects.get(id=id)
                # select * from account where username=request.user.username
                user = Account.objects.get(username=request.user.username)
                # select * from review where komik=komik, user=user
                old_review = Review.objects.get(komik=komik, user=user)
                # delete from review where id=old_review.id;
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
                # select * from account where username=request.user.username
                user = Account.objects.get(username=request.user.username)
                # select * from list where id=id, user=user.username
                list = List.objects.get(id=id, user=user)
            except List.DoesNotExist:
                raise Http404("List does not exist!")
        return render(request, 'komikrepo/list.html', {'id': list.id, 'title': list.title, 'desc': list.description})
    return render(request, 'komikrepo/list.html')

def createList(request):
    if request.method == 'POST':
        form = ListCreateForm(request.POST)
        print(form.is_valid())
        if form.is_valid() and request.user.is_authenticated:
            print('found one ' + str(form.cleaned_data.get('title')))
            try:
                # select * from account where username=request.user.username
                user = Account.objects.get(username=request.user.username)
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')

                l = List(user=user, title=title, description=description, list_size=0)
                # insert into list (title, description, list_size, user_id) values (title,description, 0, user.username);
                l.save()

            except Account.DoesNotExist:
                raise Http404("Account does not exist!")
            return redirect('/list/edit/'+str(l.id))
        else:
            return render(request, 'komikrepo/createlist.html', {'form': form})
    else:
        form = ListCreateForm()
        return render(request, 'komikrepo/createlist.html', {'form': form})
    return render(request, 'komikrepo/list.html')


def deleteList(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated and id:
            try:
                # select * from account where username=request.user.username;
                user = Account.objects.get(username=request.user.username)
                list = List.objects.get(id=id, user=user)
                # delete from list where id=list.id, user=list.user;
                list.delete()
                success = True
                print('list deleted')
            except List.DoesNotExist or Account.DoesNotExist:
                raise Http404("Error retreiving from DB")
                success = False
    else:
        success = False
    print(success)
    return render(request, 'komikrepo/deletelist.html', {'success': success})



def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        # select * from komik where title like q order by title;
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
        # select * from account where username=request.user.username;
        user = Account.objects.get(username=request.user.username)
        # select * from list where user=user.username, id=request.id;
        list = List.objects.get(user=user, id=request.GET.get('id', None))
        results = []
        # select * from listrank where list=list.id order by ranking;
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
            # select * from account where username=request.user.username;
            user = Account.objects.get(username=request.user.username)
            # select * from list where user=user.id, id=request.id;
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            # select * from komik where id=request.komik_id;
            komik = Komik.objects.get(id=request.POST.get('komik_id', None))
            listrank = ListRank(list=list, komik=komik,  ranking=request.POST.get('ranking', 1), description="")
            # insert into listrank (ranking, description, komik_id, list_id) values (form.ranking, '', komik.id, list.id);
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
            # select * from account where username=request.user.username;
            user = Account.objects.get(username=request.user.username)
            # select * from list where user=user.id, id=request.id;
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            # select * from komik where id=request.komik_id;
            komik = Komik.objects.get(id=request.POST.get('komik_id', None))
            # select * from listrank where komik=komik.id, list=list.id;
            listrank = ListRank.objects.get(komik=komik, list=list)
            rank = listrank.ranking
            # delete from listrank where id=listrank.id;
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
            # select * from account where username=request.user.username;
            user = Account.objects.get(username=request.user.username)
            # select * from list where user=user.id, id=request.id;
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            sorted = json.loads(request.POST.get('komik_sort', None))
            print(sorted)
            for index, id in enumerate(sorted, start=1):
                # switches ranking of listrank records (lr1, lr2)
                # update listrank set ranking=lr2.ranking where id=lr1.id;
                # update listrank set ranking=lr1.ranking where id=lr2.id;
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
            # select * from account where username=request.user.username;
            user = Account.objects.get(username=request.user.username)
            # select * from list where user=user.id, id=request.id;
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            # select * from komik where id=request.komik_id;
            komik = Komik.objects.get(id=request.POST.get('komik_id', None))
            # select * from listrank where komik_id=komik.id, list_id=list.id;
            listrank = ListRank.objects.get(komik=komik, list=list)
            listrank.description = request.POST.get('description', '')
            # update listrank set description=request.description where id=listrank.id;
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

def updateTitle(request):
    print ('dafuq')
    if request.user.is_authenticated and request.is_ajax():
        print('pass')
        try:
            # select * from account where username=request.user.username;
            user = Account.objects.get(username=request.user.username)
            # select * from list where user=user.id, id=request.id;
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            # select * from komik where id=request.komik_id;
            list.title = request.POST.get('title', None)
            # update list set title=request.title where id=list.id;
            list.save()
            data = {'result' : 'success'}
            data = json.dumps(data);
        except Account.DoesNotExist or List.DoesNotExist or Komik.DoesNotExist:
            data = {'result' : 'fail'}
            data = json.dumps(data);
    else:
        data = {'result' : 'fail'}
        data = json.dumps(data);
    return HttpResponse(data)

def updateListDesc(request):
    print ('dafuq')
    if request.user.is_authenticated and request.is_ajax():
        print('pass')
        try:
            # select * from account where username=request.user.username;
            user = Account.objects.get(username=request.user.username)
            # select * from list where user=user.id, id=request.id;
            list = List.objects.get(user=user, id=request.POST.get('id', None))
            # select * from komik where id=request.komik_id;
            list.description = request.POST.get('desc', None)
            # update list set description=request.description where id=list.id;
            list.save()
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
                # select * from list where title like '%form.search%' order by title asc;
                list_list = List.objects.filter(title__icontains=request.GET.get('search')).order_by('title')
            else:
                # select * from list order by title asc;
                list_list = List.objects.all().order_by('title')

            if(request.GET.get('sort')):
                # this does not query the DB anymore
                order = request.GET.get('sort', '')
                if order == 'abc':
                    list_list = list_list.order_by('title')
                elif order == 'cba':
                    print('print descending')
                    list_list = list_list.order_by('-title')
                elif order == 'new':
                    list_list = list_list.order_by('-created')
                elif order == 'old':
                    list_list = list_list.order_by('created')

        else:
            # select * from list order by title asc;
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
        # select * from list where id=request.id;
        list = List.objects.get(id=id)
        # select * from listrank where list=list.id order by ranking asc;
        listrank = ListRank.objects.filter(list=list).order_by('ranking')
    except List.DoesNotExist:
        raise Http404("Komik does not exist")
    if request.user.is_authenticated and request.user.username == list.user:
        canAdd = True
    else:
        canAdd = False
    return render(request, 'komikrepo/listview.html', {'list': list, 'listrank': listrank, 'canAdd': canAdd })
