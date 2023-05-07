from .models import Post, Category
from rest_framework import serializers


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.user.username')

    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'content', 'rating', 'author', 'dt_created', 'categories']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.user.username')

    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'content', 'rating', 'author', 'dt_created', 'categories']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
