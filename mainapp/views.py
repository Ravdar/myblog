from django.shortcuts import (
    render,
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
)
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from .models import Article, Comment
from .forms import CreateArticle, CreateComment


def is_superuser(user):
    return user.is_superuser


def access_denied_view(response):
    return HttpResponse("Something went wrong :(")


def home_view(response):
    list_of_articles = Article.objects.filter(is_in_polish=False)[::-1]
    return render(response, "mainapp/base.html", {"list_of_articles": list_of_articles})


def home_view_pl(response):
    list_of_articles = Article.objects.filter(is_in_polish=True)[::-1]
    return render(
        response, "mainapp/basepl.html", {"list_of_articles": list_of_articles}
    )


def article_view(response, article_id):
    article = get_object_or_404(Article, pk=article_id)
    comments = Comment.objects.filter(article=article)
    admin_name = "ravdar (op)" if response.user.is_superuser else None
    if response.method == "POST":
        form = CreateComment(response, response.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publication_date = timezone.now()
            comment.article = article
            comment = form.save()
            form = CreateComment(response, initial_author=admin_name)
    else:
        form = CreateComment(response, initial_author=admin_name)
    return render(
        response,
        "mainapp/displayarticle.html",
        {"article": article, "form": form, "comments": comments},
    )


def article_view_url(response, article_url):
    article = get_object_or_404(Article, url=article_url)
    comments = Comment.objects.filter(article=article)
    admin_name = "ravdar (op)" if response.user.is_superuser else None
    if response.method == "POST":
        form = CreateComment(response, response.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publication_date = timezone.now()
            comment.article = article
            comment = form.save()
            form = CreateComment(response, initial_author=admin_name)
    else:
        form = CreateComment(response, initial_author=admin_name)
    if article.is_in_polish == True:
        return render(
            response,
            "mainapp/displayarticlepl.html",
            {"article": article, "form": form, "comments": comments},
        )
    else:
        return render(
            response,
            "mainapp/displayarticle.html",
            {"article": article, "form": form, "comments": comments},
        )


@user_passes_test(is_superuser, login_url="mainapp:access_denied")
def new_article_view(response):
    if response.method == "POST":
        form = CreateArticle(response.POST, response.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.publication_date = timezone.now()
            article = form.save()
            return HttpResponseRedirect(
                reverse("mainapp:article_view_url", args=(article.url,))
            )
    else:
        form = CreateArticle()
    return render(response, "mainapp/newarticle.html", {"form": form})


@user_passes_test(is_superuser, login_url="mainapp:access_denied")
def edit_article_view(response, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if response.method == "POST":
        form = CreateArticle(response.POST, response.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.last_edit_date = timezone.now()
            article = form.save()

            return HttpResponseRedirect(
                reverse("mainapp:article_view", args=(article_id,))
            )
    else:
        form = CreateArticle(instance=article)

    return render(response, "mainapp/editarticle.html", {"form": form})


@user_passes_test(is_superuser, login_url="mainapp:access_denied")
def delete_article_view(response, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.delete()

    return redirect("mainapp:home_view")
