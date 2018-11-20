from django.shortcuts import render, redirect
from django.http import HttpResponse
from komikrepo.forms import *
from komikrepo.models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.core.exceptions import PermissionDenied


def index(request):
    context = {'hello': 'Test'}
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
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def accountView(request, username):
    result = Account.objects.get(username=username)
    context = {'account': result.username, 'description': result.description }
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
                komik_list = Komik.objects.filter(title__icontains=request.GET.get('search'))
            else:
                komik_list = Komik.objects.all()
            for entry in request.GET:
                if entry != 'search':
                    komik_list = komik_list.filter(komik_tags=Tag.objects.filter(name=entry)[0])
                    print(komik_list)
        else:
            komik_list = Komik.objects.all()

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
