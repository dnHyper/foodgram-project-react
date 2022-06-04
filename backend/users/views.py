from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination


class CustomUserViewSet(UserViewSet):
    pagination_class = PageNumberPagination
