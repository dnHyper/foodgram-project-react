from django_filters import CharFilter, FilterSet
from django_filters import rest_framework as filters
from recipes.models import Recipes


class RecipesFilter(FilterSet):
    """Фильтрация по автору, тэгу, избранному и добавленному в покупки."""
    author = CharFilter(
        field_name='author__id',
    )
    tags = CharFilter(
        field_name='tags__slug',
    )
    is_favorited = filters.BooleanFilter(
        method='favorited_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='cart_filter'
    )

    def favorited_filter(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__author=self.request.user)
        return queryset

    def cart_filter(self, queryset, name, value):
        if value:
            return queryset.filter(cart__author=self.request.user)
        return queryset

    class Meta:
        model = Recipes
        fields = ('tags', 'author', 'is_favorited')
