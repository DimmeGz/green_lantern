from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(required=False)


class ArticleImageForm(forms.Form):
    image = forms.ImageField(required=False)


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea, label='Text')
