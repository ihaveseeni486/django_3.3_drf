from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    art_list = Article.objects.all().prefetch_related('tags')
    context = {
        'object_list': art_list
    }

    return render(request, template, context)
