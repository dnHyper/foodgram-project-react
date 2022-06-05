import reportlab
from api.filter import RecipesFilter
from api.mixins import ViewOnlyViewSet
from api.permissions import IsAuthorOrAdminOrModeratorPermission
from api.serializers import (ActionsSerializer, IngredientsSerializer,
                             RecipesSerializer, RecipesSerializerCreate,
                             TagsSerializer)
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.settings import MEDIA_ROOT, SITE_NAME
from recipes.models import (Cart, Favorite, Ingredient, IngredientInRecipe,
                            Recipes, Tag)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


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
    filterset_class = RecipesFilter

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
        get_cart = IngredientInRecipe.objects.filter(
            recipe__cart__author=request.user
        ).values(
            'ingredient__name',
            'amount',
            'ingredient__measurement_unit'
        ).annotate(
            Sum('amount')
        )
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment;'
        reportlab.rl_config.TTFSearchPath.append(str(MEDIA_ROOT) + '/fonts')
        pdfmetrics.registerFont(TTFont('Open Sans', 'opensans.ttf'))
        text_cart = ""
        for value in get_cart:
            text_cart += (
                value['ingredient__name'] + " ("
                + value['ingredient__measurement_unit'] + ") — "
                + str(value['amount__sum']) + "<br />"
            )

        pdf = SimpleDocTemplate(
            response,
            title=f"Список рецептов с сайта {SITE_NAME}",
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='Top Recipe',
            fontName='Open Sans',
            fontSize=15,
            leading=20,
            backColor=colors.blueviolet,
            textColor=colors.white,
            alignment=TA_CENTER)
        )
        styles.add(ParagraphStyle(
            name='Ingredient',
            fontName='Open Sans',
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT)
        )
        styles.add(ParagraphStyle(
            name='Info',
            fontName='Open Sans',
            fontSize=9,
            textColor=colors.silver,
            alignment=TA_LEFT)
        )
        pdf_generate = []
        text_title = 'Ингридиенты:'
        text_info = f'Этот список был сгенерирован на сайте <b>{SITE_NAME}</b>'
        pdf_generate.append(Paragraph(text_info, styles['Ingredient']))
        pdf_generate.append(Spacer(1, 1))
        pdf_generate.append(Paragraph(text_title, styles["Top Recipe"]))
        pdf_generate.append(Spacer(1, 24))
        pdf_generate.append(Paragraph(text_cart, styles['Ingredient']))
        pdf.build(pdf_generate)
        return response
