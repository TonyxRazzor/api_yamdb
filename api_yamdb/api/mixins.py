from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):

    """
    Набор представлений, который предоставляет действия по умолчанию.
    list():
    Возвращает список всех существующих объектов.

    create():
    Создать новый объект.

    destroy():
    Удалить существующий объект.
    """
