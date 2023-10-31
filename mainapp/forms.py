from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

import re
from .views import Article, Comment
from ckeditor.widgets import CKEditorWidget


class CreateArticle(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "body", "is_in_polish", "article_image", "url"]

    def __init__(self, *args, **kwargs):
        super(CreateArticle, self).__init__(*args, **kwargs)


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "text"]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        initial_author = kwargs.pop("initial_author", None)
        super(CreateComment, self).__init__(*args, **kwargs)

        if initial_author is not None:
            self.fields["author"].initial = initial_author

    def clean_author(self):
        user = self.request.user
        author = self.cleaned_data["author"]
        if re.search(r"[()]+", author) and not user.is_superuser:
            raise ValidationError("Regular user cannot use this nickname")
        return author

