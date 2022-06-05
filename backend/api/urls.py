from api.views import IngredientsViewSet, RecipesViewSet, TagsViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter


app_name = 'api'

router = DefaultRouter()

router.register('recipes', RecipesViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls')),
]
