from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from . import enums


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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-published',)
        verbose_name = 'Postagem'
        verbose_name_plural = 'Postagens'
