from django.conf.urls import url,include
from . import views
from django.contrib.auth.views import logout,login
from .feeds import LatestEntriesFeed
urlpatterns = [
    url(r'^rss/feeds/$', LatestEntriesFeed()),
    url(r'^$',views.homepage,name='homepage'),
    url(r'^login/$',login,{'template_name': 'Music/login.html'},name='login'),
    url(r'^signup/$', views.signup,name='signup'),
    url(r'^userhome/$', views.userhome, name='userhome'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^albums/$', views.albums, name='albums'),
    url(r'^genres/$', views.genres, name='genres'),
    url(r'^artists/$', views.artists, name='artists'),
    url(r'^addalbum/$',views.addalbum,name='addalbum'),
    url(r'^addsong/$',views.addsong,name='addsong'),
    url(r'^logout/$',logout,{'next_page': 'homepage'},name='logout'),
    url(r'^albums/(?P<album_id>[0-9]+)/$',views.showalbum,name='showalbum'),
    url(r'^songs/(?P<song_id>[0-9]+)/$',views.showsong,name='showsong'),
    url(r'^genres/(?P<genre_name>[a-zA-Z0-9 &]+)/$',views.genreinfo,name='genreinfo'),
    url(r'^artists/(?P<artist_name>[a-zA-Z0-9 &]+)/$',views.artistinfo,name='artistinfo'),
    url(r'^feedback/$',views.feedback,name='feedback'),
    #url(r'^showfeedback/$',views.showfeedback,name='showfeedback'),
    url(r'^search/$',views.search,name='search'),
    url(r'^aboutus/$',views.aboutus,name='aboutus'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^recommend/$',views.recommend,name='recommend'),
    url(r'^favourites/$',views.favourites,name='favourites'),
    #url(r'^like/(?P<song_id>[0-9]+)/$',views.like,name='like'),
    #url(r'^dislike/(?P<song_id>[0-9]+)/$',views.dislike,name='dislike'),
]
