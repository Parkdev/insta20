from django.db import models

# Create your models here.
from config import settings


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    comment = models.TextField('코맨트')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='post_images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='post', verbose_name='이미지')


class Locations(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    name = models.CharField('위치명', max_length=100)
    latitude = models.CharField('위도', max_length=100)
    longitude = models.CharField('경도', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '위치'
        verbose_name_plural = f'{verbose_name} 목록'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='포스트',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자'
    )
    content = models.TextField('댓글')
    tags = models.ManyToManyField(
        'HashTag',
        blank=True,
        verbose_name='해쉬태그'
    )

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'


class HashTag(models.Model):
    name = models.CharField('태그명', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '해쉬태그'
        verbose_name_plural = f'{verbose_name} 목록'
