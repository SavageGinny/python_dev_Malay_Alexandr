from django.db import models

# Create your models here.
class User(models.Model):
    """
    Модель для пользователя в приложении 'blogs'.

    Представляет пользователя, который может владеть блогами и оставлять комментарии. Каждый пользователь
    имеет уникальный логин и email.

    Атрибуты:
        login (CharField): Логин пользователя. Уникален для каждого пользователя.
        email (EmailField): Электронная почта пользователя.

    Метаданные:
        db_table (str): Имя таблицы в базе данных — 'Users'.
        app_label (str): Метка приложения, к которому принадлежит модель — 'blogs'.
        managed (bool): Указывает, что эта модель не управляется Django (не создается и не мигрируется автоматически).
    """
    login = models.CharField(max_length=255, unique=True)
    email = models.EmailField()

    class Meta:
        db_table = 'Users'
        app_label = 'blogs'
        managed = False


class Blog(models.Model):
    """
    Модель для блога в приложении 'blogs'.

    Представляет блог, принадлежащий пользователю. В каждом блоге содержатся различные посты.

    Атрибуты:
        owner (ForeignKey): Внешний ключ, указывающий на пользователя, который является владельцем блога.
        name (CharField): Название блога.
        description (TextField): Описание блога.

    Метаданные:
        db_table (str): Имя таблицы в базе данных — 'Blog'.
        app_label (str): Метка приложения, к которому принадлежит модель — 'blogs'.
        managed (bool): Указывает, что эта модель не управляется Django (не создается и не мигрируется автоматически).
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'Blog'
        app_label = 'blogs'
        managed = False


class Post(models.Model):
    """
    Модель для поста в блоге в приложении 'blogs'.

    Представляет пост, который был опубликован в блоге. Каждый пост связан с определенным пользователем
    (автором) и блогом.

    Атрибуты:
        header (CharField): Заголовок поста.
        text (TextField): Текст поста.
        author (ForeignKey): Внешний ключ, указывающий на пользователя, который является автором поста.
        blog (ForeignKey): Внешний ключ, указывающий на блог, в котором был опубликован пост.

    Метаданные:
        db_table (str): Имя таблицы в базе данных — 'Post'.
        app_label (str): Метка приложения, к которому принадлежит модель — 'blogs'.
        managed (bool): Указывает, что эта модель не управляется Django (не создается и не мигрируется автоматически).
    """
    header = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Post'
        app_label = 'blogs'
        managed = False
