from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from Music.models import Album


class LatestEntriesFeed(Feed):
    title = "Buzz Music RSS Feed"
    link = "//"
    description = "Updates on changes and additions to Buzz Music."

    def items(self):
        return Album.objects.order_by('-pk')[:5]

    def item_title(self, item):
        return item.album_name

    def item_description(self,item):
        return item.album_artist+" "+item.album_genre


    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('showalbum', args=[item.pk])