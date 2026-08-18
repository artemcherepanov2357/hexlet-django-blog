from django import forms  # Импортируем формы Django


class CommentArticleForm(forms.Form):
    content = forms.CharField(label="Комментарий", max_length=200)  # Текст комментария