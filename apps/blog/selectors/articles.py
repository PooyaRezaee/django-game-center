from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from ..models import Article

def get_articles():
    return Article.objects.filter(is_draft=False)

def get_article(slug,show_draft=False):
    try:
        article = Article.objects.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404
    
    if article.is_draft and not show_draft:
        raise Http404
    return article