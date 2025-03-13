from django.test import TestCase
from .models import *
from django.utils.timezone import now

class SpaceTypeTest(TestCase):
    """
    Тесты для модели SpaceType.

    Проверяет корректное создание типов пространств и их уникальность.
    """
    databases = ['logs_db']

    def setUp(self):
        """Создаёт тестовый тип пространства."""
        self.space_type = SpaceType.objects.using('logs_db').create(name='glo')

    def test_space_type_creation(self):
        """Проверяет создание типа пространства."""
        space = SpaceType.objects.using('logs_db').get(name='glo')
        self.assertEqual(space.name, 'glo')
        self.assertTrue(SpaceType.objects.using('logs_db').filter(name='glo').exists())

    def test_unique_space_type(self):
        """Проверяет, что нельзя создать два типа пространства с одинаковым названием."""
        with self.assertRaises(Exception):
            SpaceType.objects.using('logs_db').create(name='glo')


class EventTypeTest(TestCase):
    """
    Тесты для модели EventType.

    Проверяет корректное создание типов событий и их уникальность.
    """
    databases = ['logs_db']

    def setUp(self):
        """Создаёт тестовый тип события."""
        self.event_type = EventType.objects.using('logs_db').create(name='log')

    def test_event_type_creation(self):
        """Проверяет создание типа события."""
        event = EventType.objects.using('logs_db').get(name='log')
        self.assertEqual(event.name, 'log')
        self.assertTrue(EventType.objects.using('logs_db').filter(name='log').exists())

    def test_unique_event_type(self):
        """Проверяет, что нельзя создать два типа события с одинаковым названием."""
        with self.assertRaises(Exception):
            EventType.objects.using('logs_db').create(name='log')


class LogTest(TestCase):
    """
    Тесты для модели Log.

    Проверяет корректное создание логов и их связи с типами пространств и событий.
    """
    databases = ['logs_db']

    def setUp(self):
        """Создаёт тестовые данные для логов."""
        self.space_type = SpaceType.objects.using('logs_db').create(name='poster')
        self.event_type = EventType.objects.using('logs_db').create(name='commenter')
        self.log = Log.objects.using('logs_db').create(
            datetime=now(),
            user_id=7,
            space_type=self.space_type,
            event_type=self.event_type,
            space_id=52
        )

    def test_log_creation(self):
        """Проверяет создание лога."""
        log = Log.objects.using('logs_db').get(user_id=7, space_id=52)
        self.assertEqual(log.space_type, self.space_type)
        self.assertEqual(log.event_type, self.event_type)
        self.assertEqual(log.user_id, 7)
        self.assertEqual(log.space_id, 52)
        self.assertTrue(Log.objects.using('logs_db').filter(user_id=7, space_id=52).exists())

    def test_log_space_type_relation(self):
        """Проверяет связь лога с типом пространства."""
        self.assertEqual(self.log.space_type.name, 'poster')

    def test_log_event_type_relation(self):
        """Проверяет связь лога с типом события."""
        self.assertEqual(self.log.event_type.name, 'commenter')
