from django_filters import CharFilter, FilterSet
from recipes.models import Recipes


class RecipesFilter(FilterSet):
    author = CharFilter(
        field_name='author__id',
    )
    tags = CharFilter(
        field_name='tags__slug',
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'author',)
