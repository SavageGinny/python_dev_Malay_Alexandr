from django.db.models import Model

class BlogsDBRouter:
    """
    Маршрутизатор для базы данных 'blogs_db'.

    Этот класс управляет маршрутизацией запросов к базе данных, которая используется для
    работы с приложением 'blogs'. Он определяет, какая база данных будет использоваться для
    чтения и записи данных, а также запрещает использование отношений между моделями из разных БД.

    Методы:
        db_for_read(model, **hints):
            Определяет базу данных для операций чтения (SELECT).
            Возвращает 'blogs_db', если модель относится к приложению 'blogs'.

        db_for_write(model, **hints):
            Определяет базу данных для операций записи (INSERT, UPDATE, DELETE).
            Возвращает 'blogs_db', если модель относится к приложению 'blogs'.

        allow_relation(obj1, obj2, **hints):
            Определяет, разрешено ли устанавливать отношения между моделями из разных баз данных.
            Возвращает None, что означает запрет отношений между моделями из разных БД.

        allow_migrate(db, app_label, model_name=None, **hints):
            Определяет, разрешена ли миграция для базы данных 'blogs_db'.
            Возвращает False, что запрещает миграции для базы данных 'blogs_db'.
    """

    def db_for_read(self, model: type[Model], **hints) -> str | None:
        """
        Определяет, какую базу данных использовать для операций чтения.

        Аргументы:
            model (Model): Модель, для которой необходимо выполнить операцию.
            **hints: Дополнительные параметры для маршрутизации.

        Возвращает:
            str: Название базы данных, если модель принадлежит приложению 'blogs', иначе None.
        """
        if model._meta.app_label == 'blogs':
            return 'blogs_db'
        return None

    def db_for_write(self, model: type[Model], **hints) -> str | None:
        """
        Определяет, какую базу данных использовать для операций записи.

        Аргументы:
            model (Model): Модель, для которой необходимо выполнить операцию.
            **hints: Дополнительные параметры для маршрутизации.

        Возвращает:
            str: Название базы данных, если модель принадлежит приложению 'blogs', иначе None.
        """
        if model._meta.app_label == 'blogs':
            return 'blogs_db'
        return None

    def allow_relation(self, obj1: type[Model], obj2: type[Model], **hints) -> None:
        """
        Определяет, разрешены ли отношения между моделями из разных баз данных.

        Аргументы:
            obj1 (Model): Первая модель.
            obj2 (Model): Вторая модель.
            **hints: Дополнительные параметры для проверки.

        Возвращает:
            None: Запрещает связи между моделями из разных баз данных.
        """
        return None

    def allow_migrate(self, db: str, app_label: str, model_name: str | None = None, **hints) -> bool | None:
        """
        Определяет, разрешена ли миграция для приложения 'blogs' в базе данных 'blogs_db'.

        Аргументы:
            db (str): Название базы данных.
            app_label (str): Метка приложения.
            model_name (str, optional): Название модели.
            **hints: Дополнительные параметры для проверки миграции.

        Возвращает:
            bool: Возвращает False, чтобы запретить миграции для базы данных 'blogs_db'.
        """
        if app_label == 'blogs':
            return False
        return None

class LogsDBRouter:
    """
    Маршрутизатор для базы данных 'logs_db'.

    Этот класс управляет маршрутизацией запросов к базе данных, которая используется для
    работы с приложением 'logs'. Он определяет, какая база данных будет использоваться для
    чтения и записи данных, а также запрещает использование отношений между моделями из разных БД.

    Методы:
        db_for_read(model, **hints):
            Определяет базу данных для операций чтения (SELECT).
            Возвращает 'logs_db', если модель относится к приложению 'logs'.

        db_for_write(model, **hints):
            Определяет базу данных для операций записи (INSERT, UPDATE, DELETE).
            Возвращает 'logs_db', если модель относится к приложению 'logs'.

        allow_relation(obj1, obj2, **hints):
            Определяет, разрешено ли устанавливать отношения между моделями из разных баз данных.
            Возвращает None, что означает запрет отношений между моделями из разных БД.

        allow_migrate(db, app_label, model_name=None, **hints):
            Определяет, разрешена ли миграция для базы данных 'logs_db'.
            Возвращает False, что запрещает миграции для базы данных 'logs_db'.
    """

    def db_for_read(self, model: type[Model], **hints) -> str | None:
        """
        Определяет, какую базу данных использовать для операций чтения.

        Аргументы:
            model (Model): Модель, для которой необходимо выполнить операцию.
            **hints: Дополнительные параметры для маршрутизации.

        Возвращает:
            str: Название базы данных, если модель принадлежит приложению 'logs', иначе None.
        """
        if model._meta.app_label == 'logs':
            return 'logs_db'
        return None

    def db_for_write(self, model: type[Model], **hints) -> str | None:
        """
        Определяет, какую базу данных использовать для операций записи.

        Аргументы:
            model (Model): Модель, для которой необходимо выполнить операцию.
            **hints: Дополнительные параметры для маршрутизации.

        Возвращает:
            str: Название базы данных, если модель принадлежит приложению 'logs', иначе None.
        """
        if model._meta.app_label == 'logs':
            return 'logs_db'
        return None

    def allow_relation(self, obj1: type[Model], obj2: type[Model], **hints) -> None:
        """
        Определяет, разрешены ли отношения между моделями из разных баз данных.

        Аргументы:
            obj1 (Model): Первая модель.
            obj2 (Model): Вторая модель.
            **hints: Дополнительные параметры для проверки.

        Возвращает:
            None: Запрещает связи между моделями из разных баз данных.
        """
        return None

    def allow_migrate(self, db: str, app_label: str, model_name: str | None = None, **hints) -> bool | None :
        """
        Определяет, разрешена ли миграция для приложения 'logs' в базе данных 'logs_db'.

        Аргументы:
            db (str): Название базы данных.
            app_label (str): Метка приложения.
            model_name (str, optional): Название модели.
            **hints: Дополнительные параметры для проверки миграции.

        Возвращает:
            bool: Возвращает False, чтобы запретить миграции для базы данных 'logs_db'.
        """
        if app_label == 'logs':
            return False
        return None


