from django_filters import rest_framework as filters

from .models import Announcement


class AnnouncementFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Announcement
        fields = ["title"]
