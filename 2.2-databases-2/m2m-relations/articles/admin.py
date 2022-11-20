from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
import collections
from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_main_topics = 0
        list_unic = []
        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data['is_main']:
                    count_main_topics += 1
                list_unic.append(form.cleaned_data['tag'])
        list_not_unic = [item for item, count in collections.Counter(list_unic).items() if count > 1]
        if len(list_not_unic) > 0:
            raise ValidationError('Тэги должны быть уникальными')
        if count_main_topics == 0:
            raise ValidationError('Должен быть хотя бы один основной раздел статьи')
        if count_main_topics > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'str_tags']
    list_filter = ['scopes']
    ordering = ['title', 'published_at']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

