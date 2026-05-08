import django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):

    author = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains'
    )

    genre = django_filters.CharFilter(
        field_name='genre__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Book
        fields = ['author', 'genre']