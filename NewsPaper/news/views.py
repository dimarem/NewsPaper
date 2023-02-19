from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from .models import Post, Author
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


class NewsCreate(CreateView):
    """Класс отвечающий за отображение формы создания статьи с типом 'NE'."""
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = Post.NEWS

        if self.request.user.is_authenticated:
            news.author = Author.objects.get(pk=self.request.user.id)
        else:
            news.author = Author.objects.get(user__name='Anonymous')

        return super().form_valid(form)


class NewsUpdate(UpdateView):
    """Класс отвечающий за отображение формы изменения статьи с типом 'NE'."""
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    """Класс отвечающий за подтверждение удаления статьи с типом 'NE'."""
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleCreate(CreateView):
    """Класс отвечающий за отображение формы создания статьи с типом 'AR'."""
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = Post.ARTICLE

        if self.request.user.is_authenticated:
            news.author = Author.objects.get(pk=self.request.user.id)
        else:
            news.author = Author.objects.get(user__name='Anonymous')

        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    """Класс отвечающий за отображение формы изменения статьи с типом 'AR'."""
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(DeleteView):
    """Класс отвечающий за подтверждение удаления статьи с типом 'AR'."""
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')
