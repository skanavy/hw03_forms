from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        Post.objects.create(
            text='Тестовый текст',
            author=User.objects.create_user(username='Stas')
        )
        Group.objects.create(
            title='группа1',
            description='desc1',
            slug='test-slug',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_slug_detail_url_exists_at_desired_location_authorized(self):
        """Страница /group/test-slug/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200)

    def profile_user_added_url_exists_at_desired_location(self):
        """Страница /profile/user доступна любому пользователю."""
        response = self.guest_client.get('/profile/user')
        self.assertEqual(response.status_code, 200)

    def profile_detail_added_url_exists_at_desired_location(self):
        """Страница /profile/user доступна любому пользователю."""
        response = self.guest_client.get('/profile/1')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def profile_edit_url_exists_at_desired_location(self):
        """Страница /profile/1/edit/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/profile/1/edit')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create')
        self.assertEqual(response.status_code, 200)
