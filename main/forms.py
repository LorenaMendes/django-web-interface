from django import forms
from .models import CrawlRequest

# class CrawlerSetup(forms.Form):
#     start_date = birth_date = forms.DateField(
#         widget=forms.TextInput(attrs={'type': 'date'})
#     )
#     end_date = birth_date = forms.DateField(
#         widget=forms.TextInput(attrs={'type': 'date'})
#     )
#     max_reqs_per_sec = forms.IntegerField(label='Max requisitions per sec', min_value=1, widget=forms.TextInput(attrs={'placeholder': '2'}))

class CrawlRequestForm(forms.ModelForm):
    class Meta:
        model = CrawlRequest

        # Options for IP rotation
        ip_type = forms.ChoiceField(required=False)
        tor_password = forms.CharField(required=False)
        proxy_list = forms.FileField(required=False)
        max_reqs_per_ip = forms.IntegerField(required=False)
        max_reuse_rounds = forms.IntegerField(required=False)
        
        # Options for User Agent rotation
        reqs_per_user_agent = forms.IntegerField(required=False)
        user_agents_file = forms.FileField(required=False)
        
        # Options for Delay
        delay_secs = forms.IntegerField(required=False)

        fields = [
            'source_name',
            'base_url',
            'antiblock',
            'captcha',
            'ip_type',
            'tor_password',
            'max_reqs_per_ip',
            'max_reuse_rounds',
            'proxy_list',
            'reqs_per_user_agent',
            'user_agents_file',
            'delay_secs',
        ]

class RawCrawlRequestForm(forms.Form):
    source_name = forms.CharField(label="Source Name", max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Example'})
    )
    base_url = forms.CharField(label="Base URL", max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'www.example.com/data/'})
    )
    antiblock = forms.ChoiceField(choices = (
        ('none', 'None'),
        ('ip', 'IP rotation'),
        ('user_agent', 'User-agent rotation'),
        ('delay', 'Delays'),
        ('cookies', 'Use cookies'),
    ))
    captcha = forms.ChoiceField(choices = (
        ('1', 'None'), 
        ('2', 'Image'),
        ('3', 'Sound'),
    ))
    
    # Options for IP rotation
    ip_type = forms.ChoiceField(required=False, choices = (
        ('tor', 'Tor'), 
        ('proxy', 'Proxy'),
    ))
    tor_password = forms.CharField(required=False, label="Tor Password", max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Password'})
    )
    proxy_list = forms.FileField(required=False, label="Proxy List")
    max_reqs_per_ip = forms.IntegerField(required=False, label="Max Requisitions per IP")
    max_reuse_rounds = forms.IntegerField(required=False, label="Max Reuse Rounds")
    
    # Options for User Agent rotation
    reqs_per_user_agent = forms.IntegerField(required=False, label="Requests per User Agent")
    user_agents_file = forms.FileField(required=False, label="User Agents File")
    delay_secs = forms.IntegerField(required=False, label="Delay in Seconds")

    # Options for Delay
    delay_secs = forms.IntegerField(required=False, label="Delay in Seconds")
