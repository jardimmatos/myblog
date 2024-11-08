from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from . import enums, managers
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, default='Título...')
    status = models.CharField(max_length=20, default=enums.StatusEnum.draft.name,
                            choices=[ (s.name, s.value) for s in enums.StatusEnum])
    slug = models.SlugField(max_length=255, unique_for_date='published')
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()
    publicados = managers.PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
        ])

    def get_share_url(self):
        return reverse('blog:share', args=[self.pk])

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Postagem'
        verbose_name_plural = 'Postagens'
        default_manager_name = 'objects'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} comentou no post {self.post}'

    class Meta:
        ordering = ('-created_at',)