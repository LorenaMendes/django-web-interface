from django import forms
from .models import CrawlRequest

# class CrawlerSetup(forms.Form):
#     source_name = forms.CharField(label="Source Name", max_length=200,
#         widget=forms.TextInput(attrs={'placeholder': 'Example'})
#     )
#     base_url = forms.CharField(label="Base URL", max_length=200,
#        widget=forms.TextInput(attrs={'placeholder': 'www.example.com/data/'})
#     )
#     start_date = birth_date = forms.DateField(
#         widget=forms.TextInput(attrs={'type': 'date'})
#     )
#     end_date = birth_date = forms.DateField(
#         widget=forms.TextInput(attrs={'type': 'date'})
#     )
#     captcha_type = forms.ChoiceField(choices = ((1, 'None'), (2, 'Image'), (3, 'Sound')))
#     antiblock = forms.ChoiceField(choices = (
#         (1, 'None'),
#         (2, 'IP rotation'),
#         (3, 'User-agent rotation'),
#         (4, 'Random delays'),
#         (5, 'Use proxy'),
#         (6, 'Use cookies'),
#     ))
#     max_reqs_per_sec = forms.IntegerField(label='Max requisitions per sec', min_value=1, widget=forms.TextInput(attrs={'placeholder': '2'}))

class CrawlRequestForm(forms.ModelForm):
    class Meta:
        model = CrawlRequest
        fields = [
            'source_name',
            'base_url'
        ]

class RawCrawlRequestForm(forms.Form):
    source_name = forms.CharField(label="Source Name", max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Example'})
    )
    base_url = forms.CharField(label="Base URL", max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'www.example.com/data/'})
    )