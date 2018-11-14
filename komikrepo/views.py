from django.shortcuts import render, redirect
from django.http import HttpResponse
from komikrepo.forms import *
from komikrepo.models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
