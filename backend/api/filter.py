from django_filters import FilterSet
from django_filters import rest_framework as filters

from recipes.models import Recipes, Tag


class RecipesFilter(FilterSet):
    """Фильтрация по автору, тэгу, избранному и добавленному в покупки."""
    author = filters.CharFilter(
        field_name='author__id',
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
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
