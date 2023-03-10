from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    """Класс описывающий модель автора статьи."""
    user = models.ForeignKey(User, models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """Обновляет рейтинг пользователя."""
        author_posts = self.posts.all()
        author_comments = self.user.comments.all()

        author_posts_total_rating = sum(map(lambda item: item.rating, author_posts))
        author_comments_total_rating = sum(map(lambda item: item.rating, author_comments))

        author_posts_comments_total_rating = 0
        for post in author_posts:
            post_comments = post.comments.all()
            author_posts_comments_total_rating += sum(map(lambda item: item.rating, post_comments))

        self.rating = author_posts_total_rating * 3 + author_comments_total_rating + author_posts_comments_total_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    """Класс описывающий модель категории новости."""
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, through='CategoryUser', related_name='subscribed_categories')

    def __str__(self):
        return f'{self.name}'


class CategoryUser(models.Model):
    """Класс описывающий модель промежуточной таблицы для реализации связи 'многие-ко-многим'
    м-у моделями пользователей и категорий новостей."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    """Класс описывающий модель новости."""
    ARTICLE = 'AR'
    NEWS = 'NE'
    TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    ]
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=ARTICLE
    )
    author = models.ForeignKey(Author, models.CASCADE, related_name='posts')
    categories = models.ManyToManyField('Category', through='PostCategory', related_name='posts')
    title = models.CharField(max_length=150)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    dt_created = models.DateTimeField(auto_now_add=True)

    def preview(self, length=124):
        """Возвращает часть статьи указанной длины."""
        return f'{self.content[0:length]}...'

    def like(self):
        """Увеличивает рейтинг на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг на единицу."""
        if self.rating:
            self.rating -= 1
            self.save()

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')


class PostCategory(models.Model):
    """Класс описывающий модель промежуточной таблицы для реализации связи 'многие-ко-многим'
    м-у моделями новостей и их категорий."""
    post = models.ForeignKey(Post, models.CASCADE)
    category = models.ForeignKey(Category, models.CASCADE)


class Comment(models.Model):
    """Класс описывающий модель комментария к новости."""
    post = models.ForeignKey(Post, models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    rating = models.IntegerField(default=0)
    dt_created = models.DateTimeField(auto_now_add=True)

    def like(self):
        """Увеличивает рейтинг на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг на единицу."""
        if self.rating:
            self.rating -= 1
            self.save()

    def __str__(self):
        return f'{self.content[:100]}...'
