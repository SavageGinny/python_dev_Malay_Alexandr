from django.contrib import admin
from .models import User, Blog, Post

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Админка для модели User.

    Этот класс управляет отображением и настройками модели `User` в административной панели Django.
    Включает в себя отображение полей, поиск по полям и настройки доступности для редактирования.

    Атрибуты:
        list_display (tuple): Список полей, которые будут отображаться в списке объектов в админке.
        search_fields (tuple): Поля, по которым можно искать записи в админке.
        readonly_fields (tuple): Поля, которые будут только для чтения и не могут быть отредактированы.
    """
    list_display = ('id', 'login', 'email')
    search_fields = ('login', 'email')
    readonly_fields = ('id', 'login', 'email')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Админка для модели Blog.

    Этот класс управляет отображением и настройками модели `Blog` в административной панели Django.
    Включает в себя отображение полей, поиск по полям, фильтрацию и настройки доступности для редактирования.

    Атрибуты:
        list_display (tuple): Список полей, которые будут отображаться в списке объектов в админке.
        search_fields (tuple): Поля, по которым можно искать записи в админке.
        list_filter (tuple): Список полей, по которым можно фильтровать записи в админке.
        readonly_fields (tuple): Поля, которые будут только для чтения и не могут быть отредактированы.
    """
    list_display = ('id', 'name', 'owner')
    search_fields = ('name', 'owner__login')
    list_filter = ('owner',)
    readonly_fields = ('id', 'owner', 'name', 'description')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админка для модели Post.

    Этот класс управляет отображением и настройками модели `Post` в административной панели Django.
    Включает в себя отображение полей, поиск по полям, фильтрацию и настройки доступности для редактирования.

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
    list_display = ('id', 'header', 'author', 'blog')
    search_fields = ('header', 'author__login', 'blog__name')
    list_filter = ('blog', 'author')
    readonly_fields = ('id', 'header', 'text', 'author', 'blog')

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
            obj (Post, optional): Запись, для которой проверяется разрешение. По умолчанию None.

        Возвращаемое значение:
            bool: False — изменение записей запрещено.
        """
        return False  # Запрещаем изменение

    def has_delete_permission(self, request, obj=None):
        """
        Запрещает удаление записей в админке.

        Аргументы:
            request (HttpRequest): HTTP-запрос.
            obj (Post, optional): Запись, для которой проверяется разрешение. По умолчанию None.

        Возвращаемое значение:
            bool: False — удаление записей запрещено.
        """
        return False  # Запрещаем удаление

