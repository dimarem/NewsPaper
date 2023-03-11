from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.cache import cache

from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm


class PostsList(ListView):
    """Класс отвечающий за отображение списка ссылок на статьи."""
    queryset = Post.objects.order_by('dt_created')
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostSearch(TemplateView):
    """Класс отвечающий за отображение поисковой формы."""
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = PostFilter()
        return context


class PostDetail(DetailView):
    """Класс отвечающий за отображение данных статьи."""
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            post_categories_ids = set(context['post'].categories.values_list('id', flat=True))
            subscribed_categories_ids = set(self.request.user.subscribed_categories.values_list('id', flat=True))

            if len(post_categories_ids.difference(subscribed_categories_ids)):
                context['subscribe'] = True
            else:
                context['subscribe'] = False

            context['categories'] = '&'.join(f"category={category_id}" for category_id in post_categories_ids)

        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    """Класс отвечающий за создание статьи с типом 'NE'."""
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = Post.NEWS

        author = Author.objects.filter(user=self.request.user).first()

        if self.request.user.is_authenticated and author:
            news.author = author
        else:
            news.author = Author.objects.get(user__username='Anonymous')

        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс отвечающий за изменение статьи с типом 'NE'."""
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    """Класс отвечающий за удаление статьи с типом 'NE'."""
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    """Класс отвечающий за создание статьи с типом 'AR'."""
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = Post.ARTICLE

        author = Author.objects.filter(user=self.request.user).first()

        if self.request.user.is_authenticated and author:
            news.author = author
        else:
            news.author = Author.objects.get(user__name='Anonymous')

        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс отвечающий за изменение статьи с типом 'AR'."""
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс отвечающий за удаление статьи с типом 'AR'."""
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def upgrade_me(request):
    """Добавить пользователя в группу авторов."""
    if not request.user.groups.filter(name='author').exists():
        Group.objects.get(name='author').user_set.add(request.user)
        Author.objects.create(user=request.user)
    return redirect('/news/')


@login_required
def subscribe_to_categories(request):
    """Подписка на категории."""
    subscribed_categories_ids = request.user.subscribed_categories.values_list('id', flat=True)
    for category_id in request.GET.getlist('category'):
        if int(category_id) not in subscribed_categories_ids:
            Category.objects.get(pk=category_id).subscribers.add(request.user)
    return render(request, 'subscription.html')


@login_required
def unsubscribe_from_categories(request):
    """Отписка от категорий."""
    subscribed_categories_ids = request.user.subscribed_categories.values_list('id', flat=True)
    for category_id in request.GET.getlist('category'):
        if int(category_id) in subscribed_categories_ids:
            Category.objects.get(pk=category_id).subscribers.remove(request.user)
    return render(request, 'unsubscription.html')
