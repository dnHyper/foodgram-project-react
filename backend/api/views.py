
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Cart, Favorite, Ingredient, Recipes, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.mixins import ViewOnlyViewSet
from api.permissions import IsAuthorOrAdminOrModeratorPermission
from api.serializers import (ActionsSerializer, IngredientsSerializer,
                             RecipesSerializer, RecipesSerializerCreate,
                             TagsSerializer)


class IngredientFilter(SearchFilter):
    search_param = 'name'


class TagsViewSet(ViewOnlyViewSet):
    """Управление тэгами."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(ViewOnlyViewSet):
    """Управление ингридиентами."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipesViewSet(viewsets.ModelViewSet):
    """Управление рецептами."""
    queryset = Recipes.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrAdminOrModeratorPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author__id', 'tags__name')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipesSerializerCreate
        return RecipesSerializer

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="shopping_cart",
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipes, id=pk)

        cart = Cart.objects.filter(
            author=user,
            recipe=recipe
        )

        if request.method == 'POST':

            if cart.exists():
                error = {
                    'errors': ('Нельзя повторно добавить рецепт в список '
                               'покупок.')
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            Cart(
                author=user,
                recipe=recipe
            ).save()
            serializer = ActionsSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not cart.exists():
            error = {
                'errors': ('Этот рецепт отсутствует в списке ваших'
                           ' покупок.')
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="favorite",
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipes, id=pk)

        favorite = Favorite.objects.filter(
            author=user,
            recipe=recipe
        )

        if request.method == 'POST':

            if favorite.exists():
                error = {
                    'errors': 'Нельзя повторно добавить рецепт в избранное.'
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            Favorite(
                author=user,
                recipe=recipe
            ).save()
            serializer = ActionsSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not favorite.exists():
            error = {'errors': 'Этот рецепт отсутствует в вашем избранном.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def download_shopping_cart(self, request):
        get_cart = Recipes.objects.filter(shopping_cart__author=request.user)

        if not get_cart:
            error = {'errors': 'У вас не сохранено ни одного рецепта.'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
