from django.test import TestCase
from django.contrib.auth.models import User
from . import models, enums
from django.utils import timezone
from django.urls import reverse
from django.core import mail


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(username='user', password='1234', email='test@test.com')

        # criando um post com status rascunho para testar o qs, posteriormente
        cls.draft_post = models.Post.objects.create(
            title="Draft Post Teste",
            slug="draft-post-teste",
            content="Conteúdo do Post",
            created_by=cls.user,
            created_at=timezone.now()
        )

        # criar outro, agora com o status de publicado
        cls.published_post = models.Post.objects.create(
            title="Published Post Teste",
            slug="published-post-teste",
            content="Conteúdo do Post publicado",
            created_by=cls.user,
            status= enums.StatusEnum.published.name,
            created_at=timezone.now()
        )

    # Testes unitários

    def test_post_str(self):
        # testar o método __str__
        self.assertEqual(str(self.draft_post), "Draft Post Teste")

    def test_get_absolute_url(self):
        # testar o get_absolute_url da instancia
        url = self.draft_post.get_absolute_url()
        expected_url = reverse('blog:detail', args=[
            self.draft_post.created_at.year,
            self.draft_post.created_at.month,
            self.draft_post.created_at.day,
            self.draft_post.slug,
            ])
        self.assertEqual(url, expected_url)

    def  test_get_share_url(self):
        shared_url = self.draft_post.get_share_url()
        expected_url = reverse('blog:share', args=[self.draft_post.pk])
        self.assertEqual(shared_url, expected_url)

    def test_default_status(self):
        self.assertEqual(self.draft_post.status, enums.StatusEnum.draft.name)


    # Testes de integração

    def test_post_creation(self):
        # validamos se há post criado
        post_count = models.Post.objects.count()
        # como foram criados 2 registros, um em cada status, podemos considerar 2
        self.assertEqual(post_count, 2)
        
    def test_manager_published(self):
        # validamos se há post criado no manager "publicados"
        posts = models.Post.publicados.all()
        # como foi criado apenas 1 registro como published, vamos considerar 1
        self.assertEqual(posts.count(), 1)
        # testar se o published_post está na lista
        self.assertIn(self.published_post, posts)
        # testar se o draft não está na lista de published
        self.assertNotIn(self.draft_post, posts)


class PostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(username='user', password='1234', email='test@test.com')

        # criando um post com status rascunho para testar o qs, posteriormente
        cls.draft_post = models.Post.objects.create(
            title="Draft Post Teste",
            slug="draft-post-teste",
            content="Conteúdo do Post",
            created_by=cls.user,
            created_at=timezone.now()
        )

        # criar outro, agora com o status de publicado
        cls.published_post = models.Post.objects.create(
            title="Published Post Teste",
            slug="published-post-teste",
            content="Conteúdo do Post publicado",
            created_by=cls.user,
            status= enums.StatusEnum.published.name,
            created_at=timezone.now()
        )

    def test_list_view(self):
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, 'Published Post Teste')
        self.assertNotContains(response, 'Draft Post Teste')


class PostDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(username='user', password='1234', email='test@test.com')

        cls.published_post = models.Post.objects.create(
            title="Published Post Teste",
            slug="published-post-teste",
            content="Conteúdo do Post publicado",
            created_by=cls.user,
            status= enums.StatusEnum.published.name,
            created_at=timezone.now()
        )

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:detail', args=[
            self.published_post.created_at.year,
            self.published_post.created_at.month,
            self.published_post.created_at.day,
            self.published_post.slug
        ]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, "Published Post Teste")
        self.assertContains(response, "Conteúdo do Post publicado")


class PostShareViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(username='user', password='1234', email='test@test.com')

        cls.published_post = models.Post.objects.create(
            title="Published Post Teste",
            slug="published-post-teste",
            content="Conteúdo do Post publicado",
            created_by=cls.user,
            status= enums.StatusEnum.published.name,
            created_at=timezone.now()
        )

    def test_post_share_view_get(self):
        response = self.client.get(reverse('blog:share', args=[
            self.published_post.pk
        ]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/share.html')
        
    def test_post_share_view_post(self):
        response = self.client \
            .post(
                reverse('blog:share', args=[self.published_post.pk]),
                {
                    'nome': 'Augustus',
                    'email': 'mail@example.com',
                    'comentario': 'Confira este post!'
                }
            )
        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(response, 'blog/share.html')
        self.assertIn("Augustus", mail.outbox[0].subject)
