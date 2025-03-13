from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from unittest.mock import patch, Mock
from django.utils.timezone import now, timedelta
from .views import *


class CommentsAPITestCase(APITestCase):
    """
    Тесты для API, собирающем данные о комментариях пользователя.

    Этот класс тестирует API, которое возвращает информацию о комментариях пользователя:
    - проверка получения данных о комментариях по логину пользователя;
    - проверка обработки ошибок, когда не передан параметр login или указан неверный логин.

    Тесты включают в себя успешное выполнение запросов, а также проверку случаев с ошибками
    (например, отсутствие логина).
    """
    databases = ['logs_db', 'blogs_db']

    def setUp(self) -> None:
        """Настройка тестовых данных для проверки работы API комментариев."""
        self.event_type = EventType.objects.using('logs_db').get(name="comment")
        self.space_type = SpaceType.objects.using('logs_db').get(name="post")
        self.user = User.objects.create(login="ChillGuy", email="ChillGuy@example.com")
        self.blog = Blog.objects.using('blogs_db').create(
            owner=self.user,
            name="Rich Blog",
            description="A blog about rich life."
        )
        self.post = Post.objects.using('blogs_db').create(
            header="First Post",
            text="This is the first post in the blog.",
            author=self.user,
            blog=self.blog
        )
        self.log = Log.objects.using('logs_db').create(
            datetime=now(),
            user_id=self.user.id,
            space_type=self.space_type,
            event_type=self.event_type,
            space_id=self.post.id
        )

    def test_comments_api(self) -> None:
        """
        Проверяет работу API для получения комментариев.

        Тестирует успешное выполнение запроса с параметром login.
        Проверяется, что возвращаются данные о комментариях пользователя.
        """
        url = reverse('comments-api')
        response = self.client.get(url, {'login': 'ChillGuy'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {"login": "ChillGuy", "header": "First Post", "author_login": "ChillGuy", "comments_count": 1}
        ])

    def test_get_comments_error_missing_login(self) -> None:
        """
        Проверяет ошибку, если параметр 'login' не передан в запросе.

        Ожидается ошибка 400 с сообщением о необходимости указания логина.
        """
        url = reverse('comments-api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Login is required'})

    def test_get_comments_error_login(self) -> None:
        """
        Проверяет ошибку, если указан неверный логин пользователя.

        Ожидается ошибка 400 с сообщением о необходимости указания логина.
        """
        url = reverse('comments-api')
        response = self.client.get(url, {'login': 'NotUser'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Login is required'})

class GeneralAPITestCase(APITestCase):
    """
    Тесты для API, собирающем данные о общей активности пользователя.

    Этот класс тестирует API, которое возвращает информацию о действиях пользователя, включая:
    - количество входов и выходов на сайт;
    - количество действий внутри блога пользователя.

    Тесты включают в себя проверку успешного выполнения запросов с параметром login, обработку ошибок (отсутствие логина или неверный логин),
    а также проверку случаев, когда для одного пользователя есть несколько записей активности на разные даты.
    """

    databases = ['logs_db', 'blogs_db']

    def setUp(self) -> None:
        """Настройка тестовых данных для проверки работы API общей активности пользователя."""
        self.login_event = EventType.objects.using('logs_db').get(name="login")
        self.global_space_type = SpaceType.objects.using('logs_db').get(name="global")
        self.create_post_event = EventType.objects.using('logs_db').get(name="create_post")
        self.delete_post_event = EventType.objects.using('logs_db').get(name="delete_post")
        self.logout_event = EventType.objects.using('logs_db').get(name="logout")
        self.blog_space_type = SpaceType.objects.using('logs_db').get(name="blog")

        self.user = User.objects.create(login="ChillGuy", email="ChillGuy@example.com")

        self.log_login = Log.objects.using('logs_db').create(
            datetime=now(),
            user_id=self.user.id,
            event_type=self.create_post_event,
            space_type=self.blog_space_type,
            space_id=1
        )

        self.log_logout = Log.objects.using('logs_db').create(
            datetime=now(),
            user_id=self.user.id,
            event_type=self.logout_event,
            space_type=self.global_space_type,
            space_id=None
        )

        self.log_blog_action = Log.objects.using('logs_db').create(
            datetime=now(),
            user_id=self.user.id,
            event_type=self.login_event,
            space_type=self.global_space_type,
            space_id=None
        )

    def test_general_api(self) -> None:
        """
        Проверяет работу API для получения общей активности пользователя.

        Тестирует успешное выполнение запроса с параметром login.
        Проверяется, что возвращаются данные о входах, выходах и действиях пользователя.
        """
        url = reverse('general-api')
        response = self.client.get(url, {'login': 'ChillGuy'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                "date": self.log_login.datetime.date().isoformat(),
                "logins": 1,
                "logouts": 1,
                "blog_actions_count": 1
            }
        ])

    def test_get_general_error_missing_login(self) -> None:
        """
        Проверяет ошибку, если параметр 'login' не передан в запросе.

        Ожидается ошибка 400 с сообщением о необходимости указания логина.
        """
        url = reverse('general-api')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Login is required'})

    def test_get_general_error_invalid_login(self) -> None:
        """
        Проверяет ошибку, если указан неверный логин пользователя.

        Ожидается ошибка 400 с сообщением о необходимости указания логина.
        """
        url = reverse('general-api')
        response = self.client.get(url, {'login': 'NonExistentUser'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Login is required'})

    def test_general_api_multiple_entries(self) -> None:
        """
        Проверяет работу API с несколькими записями для одного пользователя.

        Тестирует случай, когда для одного пользователя есть несколько записей активности.
        Проверяется, что возвращаются все записи с правильной датой и статистикой.
        """
        Log.objects.using('logs_db').create(
            datetime=now() + timedelta(days=2),
            user_id=self.user.id,
            event_type=self.delete_post_event,
            space_type=self.blog_space_type,
            space_id=1
        )
        Log.objects.using('logs_db').create(
            datetime=now() + timedelta(days=2),
            user_id=self.user.id,
            event_type=self.create_post_event,
            space_type=self.blog_space_type,
            space_id=1
        )

        url = reverse('general-api')
        response = self.client.get(url, {'login': 'ChillGuy'})

        dater = now() + timedelta(days=2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                "date": self.log_login.datetime.date().isoformat(),
                "logins": 1,
                "logouts": 1,
                "blog_actions_count": 1
            },
            {
                "date": dater.strftime('%Y-%m-%d'),
                "logins": 0,
                "logouts": 0,
                "blog_actions_count": 2
            }
        ])

class GetDataFromAPITest(TestCase):
    """
    Тесты для функции get_data_from_api.

    Этот класс тестирует функцию get_data_from_api, которая выполняет запросы к внешнему API для получения данных
    о комментариях и общей активности пользователя.

    Тесты охватывают следующие случаи:
    - успешный возврат данных с кодом ответа 200;
    - обработка ошибок API с кодом 400 (неудачные запросы);
    - частичный сбой, когда один из запросов успешен, а другой — нет.
    """

    @patch("requests.get")
    def test_successful_api_responses(self, mock_get: Mock) -> None:
        """
        Проверяет корректную обработку успешных ответов API.

        Тестирует успешный возврат данных для комментариев и общей активности пользователя.
        Проверяется правильность обработки успешных ответов с кодом 200.
        """
        mock_get.side_effect = (self.mock_response(200,
                [{"login": "ChillGuy", "header": "Python 3.12", "author_login": "user1", "comments_count": 1}]),
                self.mock_response(200,
                [{"date": "2025-03-05", "logins": 2, "logouts": 0, "blog_actions_count": 2}]))

        comments, general = get_data_from_api("ChillGuy")
        self.assertEqual(comments, [
            {"login": "ChillGuy", "header": "Python 3.12", "author_login": "user1", "comments_count": 1}])
        self.assertEqual(general, [
            {"date": "2025-03-05", "logins": 2, "logouts": 0, "blog_actions_count": 2},
        ])

    @patch("requests.get")
    def test_api_failure(self, mock_get: Mock) -> None:
        """
        Проверяет обработку ошибок API.

        Тестирует случай, когда API возвращает ошибку с кодом 400.
        Проверяется, что возвращаются пустые данные.
        """
        mock_get.side_effect = (self.mock_response(400, []), self.mock_response(400, []))

        comments, general = get_data_from_api("ChillGuy")

        self.assertEqual(comments, [])
        self.assertEqual(general, [])

    @patch("requests.get")
    def test_api_partial_failure(self, mock_get: Mock) -> None:
        """
        Проверяет обработку частичного сбоя API.

        Тестирует случай, когда один из API-запросов успешен, а другой — нет.
        Проверяется, что возвращаются корректные данные для успешного запроса.
        """
        mock_get.side_effect = (
            self.mock_response(200, [
                {"login": "ChillGuy", "header": "Python 3.12", "author_login": "user1", "comments_count": 1}
            ]),
            self.mock_response(400, [])
        )

        comments, general = get_data_from_api("ChillGuy")

        self.assertEqual(comments, [
            {"login": "ChillGuy", "header": "Python 3.12", "author_login": "user1", "comments_count": 1}
        ])
        self.assertEqual(general, [])

    def mock_response(self, status_code: int, json_data: list[dict]) -> Mock:
        """
        Мокирует ответ API.

        Создает мок-объект с заданным статусом и данными.
        """
        mock_resp = Mock()
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_data
        return mock_resp

class DownloadCSVTestCase(APITestCase):
    """
    Тесты для функции скачивания CSV-файлов.

    Этот класс тестирует функциональность скачивания CSV-файлов с данными о комментариях и общей активности пользователя.
    Он проверяет успешные случаи скачивания данных, а также обработку ошибок, например, неправильного типа данных.
    """

    @patch("UserActions.views.get_data_from_api")
    def test_download_csv_successful(self, mock_get_data_from_api: Mock) -> None:
        """
        Проверяет корректную обработку успешных запросов для скачивания CSV-файла.

        Тестирует успешный возврат данных для скачивания CSV-файла, если данные для комментариев предоставляются API.
        Проверяется, что CSV-файл правильно формируется с ожидаемым содержимым.
        """
        mock_get_data_from_api.side_effect = (
            ([
                 {"login": "ChillGuy", "header": "Python 3.12", "author_login": "user1", "comments_count": 1}
             ], [
                 {"date": "2025-03-05", "logins": 2, "logouts": 0, "blog_actions_count": 2}
             ]),)

        url = reverse("download_csv", args=["ChillGuy", "comments"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_csv = "user_login,post_header,post_author,comment count\r\nChillGuy,Python 3.12,user1,1\r\n"
        self.assertEqual(response.content.decode(), expected_csv)

    @patch("UserActions.views.get_data_from_api")
    def test_download_csv_invalid_dataset_type(self, mock_get_data_from_api: Mock) -> None:
        """
        Тестирует ошибку, если тип данных для скачивания неверен.

        Тестирует обработку ошибки при запросе неправильного типа данных для скачивания.
        Ожидается ошибка 400 с соответствующим сообщением о неверном типе данных.
        """
        mock_get_data_from_api.side_effect = (
            ([
                 {"login": "ChillGuy", "header": "Python 3.12", "author_login": "user1", "comments_count": 1}
             ], [
                 {"date": "2025-03-05", "logins": 2, "logouts": 0, "blog_actions_count": 2}
             ]),)

        url = reverse("download_csv", args=["ChillGuy", "comms"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


