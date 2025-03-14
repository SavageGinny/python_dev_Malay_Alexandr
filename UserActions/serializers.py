from rest_framework import serializers


class CommentsSerializer(serializers.Serializer):
    """
    Сериализатор для данных о комментариях пользователя.

    Этот сериализатор используется для преобразования данных о комментариях пользователя в формат JSON.

    Поля:
        login (str): Логин пользователя, который оставил комментарий.
        header (str): Заголовок поста, в котором был оставлен комментарий.
        author_login (str): Логин автора поста.
        comments_count (int): Количество комментариев, оставленных пользователем в конкретном посте.
    """
    login = serializers.CharField()
    header = serializers.CharField()
    author_login = serializers.CharField()
    comments_count = serializers.IntegerField()

class UserActivitySerializer(serializers.Serializer):
    """
    Сериализатор для данных о действиях пользователя в блоге.

    Этот сериализатор используется для преобразования данных о действиях пользователя в блоге (входы, выходы, действия) в формат JSON.

    Поля:
        date (date): Дата, на которую были зарегистрированы действия.
        logins (int): Количество входов пользователя на сайт в указанную дату.
        logouts (int): Количество выходов пользователя с сайта в указанную дату.
        blog_actions_count (int): Количество действий пользователя в блоге (например, создания постов или комментариев).
    """
    date = serializers.DateField()
    logins = serializers.IntegerField()
    logouts = serializers.IntegerField()
    blog_actions_count = serializers.IntegerField()


