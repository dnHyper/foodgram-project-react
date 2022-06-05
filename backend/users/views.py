from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import User
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from users.models import Subscriptions


class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет пользователя."""
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="subscribe",
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    )
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, id=id)
        follow = Subscriptions.objects.filter(
                user=request.user,
                following=user
        )
        if request.method == 'POST':
            if follow.exists() or user == request.user:
                error = {
                    'errors': (
                        'Вы пытаетесь подписаться на себя, или вы '
                        'уже подписаны на этого пользователя.')
                }
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            Subscriptions(
                user=request.user,
                following=user
            ).save()
            return Response(status=status.HTTP_201_CREATED)

        if not follow.exists():
            error = {
                'errors': 'Вы не были подписаны на этого человека'
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
