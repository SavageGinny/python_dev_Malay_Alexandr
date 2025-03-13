from django.contrib import admin
from .models import SpaceType, EventType, Log

@admin.register(SpaceType)
class SpaceTypeAdmin(admin.ModelAdmin):
    """
    Админка для модели SpaceType.

    Этот класс управляет отображением и настройками модели `SpaceType` в административной панели Django.
    Включает в себя отображение полей, поиск по полям и настройки доступности для редактирования.

    Атрибуты:
        list_display (tuple): Список полей, которые будут отображаться в списке объектов в админке.
        search_fields (tuple): Поля, по которым можно искать записи в админке.
        readonly_fields (tuple): Поля, которые будут только для чтения и не могут быть отредактированы.
    """
    list_display = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('id', 'name')


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """
    Админка для модели EventType.

    Этот класс управляет отображением и настройками модели `EventType` в административной панели Django.
    Включает в себя отображение полей, поиск по полям и настройки доступности для редактирования.

    Атрибуты:
        list_display (tuple): Список полей, которые будут отображаться в списке объектов в админке.
        search_fields (tuple): Поля, по которым можно искать записи в админке.
        readonly_fields (tuple): Поля, которые будут только для чтения и не могут быть отредактированы.
    """
    list_display = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('id', 'name')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """
    Админка для модели Log.

    Этот класс управляет отображением и настройками модели `Log` в административной панели Django.
    Включает в себя отображение полей, фильтрацию, поиск и настройки доступности для редактирования.

    Атрибуты:
        list_display (tuple): Список полей, которые будут отображаться в списке объектов в админке.
        search_fields (tuple): Поля, по которым можно искать записи в админке.
        list_filter (tuple): Список полей, по которым можно фильтровать записи в админке.
        readonly_fields (tuple): Поля, которые будут только для чтения и не могут быть отредактированы.

    Методы:
        has_add_permission: Запрещает добавление новых записей.
        has_change_permission: Запрещает изменение существующих записей.
        has_delete_permission: Запрещает удаление записей.
    """
    list_display = ('id', 'datetime', 'user_id', 'space_type', 'event_type', 'space_id')
    search_fields = ('user_id',)
    list_filter = ('space_type', 'event_type')
    readonly_fields = ('id', 'datetime', 'user_id', 'space_type', 'event_type', 'space_id')

    def has_add_permission(self, request):
        """
        Запрещает добавление новых записей в админке.

        Аргументы:
            request (HttpRequest): HTTP-запрос.

        Возвращаемое значение:
            bool: False — добавление новых записей запрещено.
        """
        return False  # Запрещаем добавление

    def has_change_permission(self, request, obj=None):
        """
        Запрещает изменение существующих записей в админке.

        Аргументы:
            request (HttpRequest): HTTP-запрос.
            obj (Log, optional): Запись, для которой проверяется разрешение. По умолчанию None.

        Возвращаемое значение:
            bool: False — изменение записей запрещено.
        """
        return False  # Запрещаем изменение

    def has_delete_permission(self, request, obj=None):
        """
        Запрещает удаление записей в админке.

        Аргументы:
            request (HttpRequest): HTTP-запрос.
            obj (Log, optional): Запись, для которой проверяется разрешение. По умолчанию None.

        Возвращаемое значение:
            bool: False — удаление записей запрещено.
        """
        return False  # Запрещаем удаление

