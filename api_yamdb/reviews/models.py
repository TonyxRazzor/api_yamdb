from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


from .validators import year_validator


class Category(models.Model):
    """Модель категории произведения"""

    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name[:15]}'


class Genre(models.Model):
    """Модель жанра произведения"""

    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name[:15]}'


class Title(models.Model):
    """Модель произведений"""

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )
    description = models.TextField(
        'Описание произведения',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    name = models.CharField(
        'Название',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField(
        'Год',
        validators=(year_validator, )
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name[:15]


class GenreTitle(models.Model):
    """Модель ManyToMany для связи произведений и жанров"""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genretitle',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titlegenre',
    )

    class Meta:
        models.UniqueConstraint(
            fields=['genre', 'title'],
            name='unique_follow'
        )
