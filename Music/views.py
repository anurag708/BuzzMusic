from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
from .models import Album,Song,Feedback,Like
from .forms import AddSong,AddAlbum,AddComment,FeedbackForm
from  django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import random,numpy
from sklearn.naive_bayes import GaussianNB

# Create your views here.

def aboutus(request):
    return render(request,'Music/aboutus.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/userhome')
    else:
        form = UserCreationForm()
    return render(request, 'Music/signup.html', {'form': form})

def homepage(request):
    return render(request,'Music/homepage.html')

@login_required(login_url='/login')
def favourites(request):
    favourite_songs=[]
    for i in Song.objects.all():
        a=Like.objects.filter(user=request.user,song=i)
        if len(a) and a.like:
            favourite_songs.append(a[0].song)
    return render(request,'Music/favourites.html',{'favourite_songs':favourite_songs})

@login_required(login_url='/login')
def userhome(request):
    recent_songs=Song.objects.order_by('-pk')[:6]
    favourite_songs=[]
    for i in Song.objects.all():
        a=Like.objects.filter(user=request.user,song=i)
        if len(a):
            favourite_songs.append(a[0].song)
    favourite_songs=random.sample(list(favourite_songs),min(6,len(favourite_songs)))
    return render(request,'Music/userhome.html',{'recent_songs':recent_songs,'favourite_songs':favourite_songs})

@login_required(login_url='/login')
def albums(request):
    all_albums=Album.objects.all()
    return render(request,'Music/albums.html',{'all_albums': all_albums})


@login_required(login_url='/login')
def songs(request):
    all_songs=Song.objects.all()
    return render(request,'Music/songs.html',{'all_songs' : all_songs})


@login_required(login_url='/login')
def genres(request):
    all_genres=list(set([i.album_genre for i in Album.objects.all()]))
    albums={}
    for i in all_genres:
        albums[i]=[]
    for i in Album.objects.all():
        albums[i.album_genre].append(i)
    for i in all_genres:
        albums[i]=random.choice(albums[i])
    return render(request,'Music/genres.html',{'albums' : albums})


@login_required(login_url='/login')
def addsong(request):
    if request.method=='POST':
        form = AddSong(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('addsong'))
    else:
        form=AddSong()
    return render(request, 'Music/addsong.html', {'form': form})

@login_required(login_url='/login')
def addalbum(request):
    if request.method=='POST':
        form = AddAlbum(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('addalbum'))
    else:
        form=AddAlbum()
    return render(request, 'Music/addalbum.html', {'form': form})

@login_required(login_url='/login')
def showalbum(request,album_id):
    album=get_object_or_404(Album,pk=album_id)
    artists_albums=get_list_or_404(Album,album_artist=album.album_artist)
    artists_albums.remove(album)
    if request.method=="POST":
        song_id=request.POST['song_id']
        song=get_object_or_404(Song,pk=song_id)
        a=Like.objects.filter(song=song,user=request.user)
        if len(a)==0:
            like=Like()
            like.user=request.user
            like.song=song
            like.like=False
        else:
            like=a[0]
        if request.method=="POST":
            if like.like:
                like.like=False
            else:
                like.like=True
            like.save()
    m={}
    for i in album.song_set.all():
        a=Like.objects.filter(user=request.user,song=i)
        if len(a) and a[0].like:
            m[i]=True
        else:
            m[i]=False
    return render(request, 'Music/albuminfo.html', {'album':album,'artists_albums':artists_albums,'m':m})

@login_required(login_url='/login')
def showsong(request,song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.method=='POST':
        form = AddComment(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.song=song
            form.save()
    form=AddComment()
    return render(request, 'Music/songinfo.html', {'song':song,'form':form})

@login_required(login_url='/login')
def genreinfo(request,genre_name):
    all_albums=get_list_or_404(Album,album_genre=genre_name)
    return render(request,'Music/genreinfo.html',{'all_albums':all_albums})

@login_required(login_url='/login')
def artists(request):
    all_artists=list(set([i.album_artist for i in Album.objects.all()]))
    albums={}
    for i in all_artists:
        albums[i]=[]
    for i in Album.objects.all():
        albums[i.album_artist].append(i)
    for i in all_artists:
        albums[i]=random.choice(albums[i])
    return render(request,'Music/artists.html',{'albums' : albums})

@login_required(login_url='/login')
def artistinfo(request,artist_name):
    all_albums=get_list_or_404(Album,album_artist=artist_name)
    return render(request,'Music/artistinfo.html',{'all_albums':all_albums})

@login_required(login_url='/login')
def feedback(request):
    if request.method=='POST':
        form=FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(feedback)
    else:
        form = FeedbackForm()
    return render(request,'Music/feedback.html',{'form':form})


@login_required(login_url='/login')
def search(request):
    string=request.POST['regex'].lower()
    album_list=[]
    song_list=[]
    if len(string):
        for i in Album.objects.all():
            if i.album_name.lower().find(string)!=-1:
                album_list.append(i)
            if i.album_artist.lower().find(string)!=-1:
                album_list.append(i)
            if i.album_genre.lower().find(string)!=-1:
                album_list.append(i)
        for i in Song.objects.all():
            if i.name.lower().find(string)!=-1:
                song_list.append(i)
            if i.album.album_name.lower().find(string)!=-1:
                song_list.append(i)
            if i.album.album_artist.lower().find(string)!=-1:
                song_list.append(i)
    return render(request,'Music/search.html',{'album_list':album_list,'song_list':song_list})

@login_required(login_url='/login')
def recommend(request):
    feed=[]
    predict=[]
    genre=set()
    artist=set()
    for i in Song.objects.all():
        genre.add(i.album.album_genre)
        artist.add(i.album.album_artist)
        a=Like.objects.filter(user=request.user,song=i)
        if len(a):
            feed.append(a[0])

    genremap={}
    artistmap={}
    k=1
    for i in genre:
        genremap[i]=k
        k+=1
    k=1
    for i in artist:
        artistmap[i]=k
        k+=1
    g=[]
    for i in Song.objects.all():
        a=Like.objects.filter(user=request.user,song=i)
        if len(a)==0:
            predict.append([genremap[i.album.album_genre],artistmap[i.album.album_artist]])
            g.append(i)

    X=[]
    Y=[]
    for i in feed:
        X.append([genremap[i.song.album.album_genre],artistmap[i.song.album.album_artist]]) 
        Y.append(i.like)
    X=numpy.array(X)
    Y=numpy.array(Y)
    predict=numpy.array(predict)
    clf=GaussianNB()
    clf=clf.fit(X,Y)
    final=clf.predict(predict)
    songs=[]
    for i in range(len(final)):
        if final[i]:
            songs.append(g[i])
    return render(request,'Music/recommend.html',{'songs':songs})






