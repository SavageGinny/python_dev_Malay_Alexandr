from django.test import TestCase
from .models import *


class UserTest(TestCase):
    """
    Тесты для модели User.

    Проверяет корректное создание пользователей и их уникальность.
    """
    databases = ['blogs_db']

    def setUp(self):
        self.user = User.objects.using('blogs_db').create(login='ChillGuy', email='ChillGuy@example.com')

    def test_user_creation(self):
        self.assertEqual(self.user.login, 'ChillGuy')
        self.assertEqual(self.user.email, 'ChillGuy@example.com')
        self.assertTrue(User.objects.filter(login='ChillGuy').exists())

    def test_unique_login(self):
        with self.assertRaises(Exception):
            User.objects.using('blogs_db').create(login='ChillGuy', email='ChillGuy@example.com')


class BlogTest(TestCase):
    """
    Тесты для модели Blog.

    Проверяет корректное создание блогов и их связь с пользователем.
    """
    databases = ['blogs_db']

    def setUp(self):
        """Создаёт тестового пользователя и блог."""
        self.user = User.objects.using('blogs_db').create(login='ChillGuy', email='ChillGuy@example.com')
        self.blog = Blog.objects.using('blogs_db').create(
            owner=self.user,
            name="Rich Blog",
            description="A blog about rich life."
        )

    def test_blog_creation(self):
        """Проверяет, что блог создаётся корректно."""
        blog = Blog.objects.using('blogs_db').get(name="Rich Blog")
        self.assertEqual(blog.owner, self.user)
        self.assertEqual(blog.name, "Rich Blog")
        self.assertEqual(blog.description, "A blog about rich life.")
        self.assertTrue(Blog.objects.using('blogs_db').filter(name="Rich Blog").exists())

    def test_blog_belongs_to_author(self):
        """Проверяет, что блог принадлежит правильному автору."""
        self.assertEqual(self.blog.owner.login, "ChillGuy")

class PostTest(TestCase):
    """
    Тесты для модели Post.

    Проверяет корректное создание постов и их связь с блогами и пользователями.
    """
    databases = ['blogs_db']

    def setUp(self):
        """Создаёт тестового пользователя, блог и пост."""
        self.user = User.objects.using('blogs_db').create(login='ChillGuy', email='ChillGuy@example.com')
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

    def test_post_creation(self):
        """Проверяет, что пост создаётся корректно."""
        post = Post.objects.using('blogs_db').get(header="First Post")
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.blog, self.blog)
        self.assertEqual(post.text, "This is the first post in the blog.")
        self.assertTrue(Post.objects.using('blogs_db').filter(header="First Post").exists())

    def test_post_belongs_to_blog(self):
        """Проверяет, что пост принадлежит правильному блогу."""
        self.assertEqual(self.post.blog.name, "Rich Blog")
        self.assertEqual(self.post.blog.owner, self.user)

    def test_post_belongs_to_author(self):
        """Проверяет, что пост принадлежит правильному автору."""
        self.assertEqual(self.post.author.login, "ChillGuy")
