from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["name", "body"]
        labels = {
            "name": "Название статьи",
            "body": "Содержание",
        }
        help_texts = {
            "name": "Введите название статьи (не более 200 символов)",
        }