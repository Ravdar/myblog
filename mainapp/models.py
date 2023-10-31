from django.db import models
from ckeditor.fields import RichTextField


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField(blank=True, null=True)
    publication_date = models.DateField()
    last_edit_date = models.DateField(null=True, blank=True)
    is_in_polish = models.BooleanField(default=False)
    article_image = models.ImageField(null=True, blank=True, upload_to="images/")
    url = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.CharField(max_length=20)
    text = models.TextField()
    publication_date = models.DateTimeField()

    def ___str___(self):
        return self.text

