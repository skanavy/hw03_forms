from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='NoName')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
        )
        cls.group = Group.objects.create(
            title='test_title',
            description='test_description',
            slug='test_slug'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    # Проверяем общедоступные страницы
    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_slug_detail_url_exists_at_desired_location_authorized(self):
        """Страница /group/test-slug/ доступна любому пользователю."""
        response = self.guest_client.get(reverse('posts:groups', kwargs={'slug': self.group.slug}))
        self.assertEqual(response.status_code, 200)

    def test_profile_user_added_url_exists_at_desired_location(self):
        """Страница /profile/user доступна любому пользователю."""
        response = self.guest_client.get('/profile/NoName/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_added_url_exists_at_desired_location(self):
        """Страница /posts/id доступна любому пользователю."""
        response = self.guest_client.get(reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_post_edit_url_exists_at_desired_location(self):
        """Страница /posts/<post_id>/edit/ доступна авторизованному пользователю."""
        response = self.authorized_client.get(reverse('posts:post_edit', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_wrong_uri_returns_404(self):
        response = self.client.get('/wrong/url/')
        self.assertEqual(response.status_code, 404)
