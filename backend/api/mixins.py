from rest_framework import mixins, viewsets


class ViewOnlyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для обработки только GET запросов."""
    pagination_class = None
