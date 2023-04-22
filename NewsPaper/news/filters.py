from django.forms import TextInput, DateInput
from django.utils.translation import gettext as _

from django_filters import FilterSet, CharFilter, DateTimeFilter
from .models import Post


class PostFilter(FilterSet):
    title__icontains = CharFilter(field_name='title', lookup_expr='icontains',
                                  widget=TextInput(attrs={'class': 'form-control'}), label='Наименование содержит')
    author_name = CharFilter(field_name='author', lookup_expr='user__username',
                             widget=TextInput(attrs={'class': 'form-control'}), label='Автор')
    dt_created__gt = DateTimeFilter(field_name='dt_created', lookup_expr='gt',
                                    widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                    label='Позже указанной даты')

    class Meta:
        model = Post
        fields = []
