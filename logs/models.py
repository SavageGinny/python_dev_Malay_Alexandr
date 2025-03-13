from django.db import models

# Create your models here.
class SpaceType(models.Model):
    """
    Модель для типа пространства в приложении 'logs'.

    Представляет тип пространства, в котором могут происходить события: global, blop, post.

    Атрибуты:
        name (CharField): Название типа пространства. Уникально для каждого типа.

    Метаданные:
        db_table (str): Имя таблицы в базе данных — 'space_type'.
        app_label (str): Метка приложения, к которому принадлежит модель — 'logs'.
        managed (bool): Указывает, что эта модель не управляется Django (не создается и не мигрируется автоматически).
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'space_type'
        app_label = 'logs'
        managed = False


class EventType(models.Model):
    """
    Модель для типа события в приложении 'logs'.

    Представляет тип события, которое может происходить в разных пространствах: login, comment, create_post, delete_post, logout.

    Атрибуты:
        name (CharField): Название типа события. Уникально для каждого типа.

    Метаданные:
        db_table (str): Имя таблицы в базе данных — 'event_type'.
        app_label (str): Метка приложения, к которому принадлежит модель — 'logs'.
        managed (bool): Указывает, что эта модель не управляется Django (не создается и не мигрируется автоматически).
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'event_type'
        app_label = 'logs'
        managed = False


class Log(models.Model):
    """
    Модель для логирования событий в приложении 'logs'.

    Представляет запись лога, которая описывает конкретное событие, произошедшее в определённом пространстве.
    Каждый лог содержит информацию о времени события, пользователе, типе пространства и типе события.

    Атрибуты:
        datetime (DateTimeField): Дата и время события.
        user_id (IntegerField): Идентификатор пользователя, совершившего действие. Ссылается на пользователя в другой базе данных.
        space_type (ForeignKey): Внешний ключ, указывающий на тип пространства, в котором произошло событие.
        event_type (ForeignKey): Внешний ключ, указывающий на тип события.
        space_id (IntegerField): Идентификатор пространства, в котором было совершено действие.

    Метаданные:
        db_table (str): Имя таблицы в базе данных — 'logs'.
        app_label (str): Метка приложения, к которому принадлежит модель — 'logs'.
        managed (bool): Указывает, что эта модель не управляется Django (не создается и не мигрируется автоматически).
    """
    datetime = models.DateTimeField()
    user_id = models.IntegerField()
    space_type = models.ForeignKey(SpaceType, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    space_id = models.IntegerField()

    class Meta:
        db_table = 'logs'
        app_label = 'logs'
        managed = False
