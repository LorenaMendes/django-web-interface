from django import forms
from .models import CrawlRequest

class CrawlRequestForm(forms.ModelForm):
    class Meta:
        model = CrawlRequest
        
        obey_robots = forms.BooleanField(required=False)

        # Options for IP rotation
        ip_type = forms.ChoiceField(required=False)
        proxy_list = forms.CharField(required=False)
        max_reqs_per_ip = forms.IntegerField(required=False)
        max_reuse_rounds = forms.IntegerField(required=False)
        
        # Options for User Agent rotation
        reqs_per_user_agent = forms.IntegerField(required=False)
        user_agents_file = forms.CharField(required=False)
        
        # Options for Delay
        delay_secs = forms.IntegerField(required=False)
        delay_type = forms.ChoiceField(required=False)
        
        # Options for Cookies
        cookies_file = forms.CharField(required=False)
        persist_cookies = forms.BooleanField(required=False)

        # Options for Captcha
        img_url = forms.CharField(required=False)
        img_xpath = forms.CharField(required=False)
        sound_url = forms.CharField(required=False)
        sound_xpath = forms.CharField(required=False)

        # Crawler type
        crawler_type = forms.CharField(required=False)
        explore_links = forms.BooleanField(required=False)
        link_extractor_max_depht = forms.IntegerField(required=False)
        link_extractor_allow = forms.CharField(required=False)

        fields = [
            'source_name',
            'base_url',
            'obey_robots',
            'antiblock',
            'captcha',
            'ip_type',
            'max_reqs_per_ip',
            'max_reuse_rounds',
            'proxy_list',
            'reqs_per_user_agent',
            'user_agents_file',
            'delay_secs',
            'delay_type',
            'cookies_file',
            'persist_cookies',
            'img_url',
            'img_xpath',
            'sound_url',
            'sound_xpath',
            'crawler_type',
            'explore_links',
            'link_extractor_max_depht',
            'link_extractor_allow',
        ]

class RawCrawlRequestForm(forms.Form):
    source_name = forms.CharField(label="Source Name", max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Example'})
    )
    base_url = forms.CharField(label="Base URL", max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'www.example.com/data/'})
    )
    obey_robots = forms.BooleanField(required=False, label="Obey robots.txt")
    antiblock = forms.ChoiceField(choices = (
        ('none', 'None'),
        ('ip', 'IP rotation'),
        ('user_agent', 'User-agent rotation'),
        ('delay', 'Delays'),
        ('cookies', 'Use cookies'),
    ), widget=forms.Select(attrs={'onchange': 'detailAntiblock();'}))
    captcha = forms.ChoiceField(choices = (
        ('none', 'None'), 
        ('image', 'Image'),
        ('sound', 'Sound'),
    ), widget=forms.Select(attrs={'onchange': 'detailCaptcha();'}))
    
    # Options for IP rotation
    ip_type = forms.ChoiceField(required=False, choices = (
        ('tor', 'Tor'), 
        ('proxy', 'Proxy'),
    ), widget=forms.Select(attrs={'onchange': 'detailIpRotationType();'}))
    proxy_list = forms.CharField(required=False, max_length=2000, label="Proxy List",
        widget=forms.TextInput(attrs={'placeholder': 'Paste here the content of your proxy list file'}))
    max_reqs_per_ip = forms.IntegerField(required=False, label="Max Requisitions per IP")
    max_reuse_rounds = forms.IntegerField(required=False, label="Max Reuse Rounds")
    
    # Options for User Agent rotation
    reqs_per_user_agent = forms.IntegerField(required=False, label="Requests per User Agent")
    user_agents_file = forms.CharField(required=False, max_length=2000, label="User Agents File",
        widget=forms.TextInput(attrs={'placeholder': 'Paste here the content of your user agents file'}))
    delay_secs = forms.IntegerField(required=False, label="Delay in Seconds")

    # Options for Delay
    delay_secs = forms.IntegerField(required=False, label="Delay in Seconds")
    delay_type = forms.ChoiceField(required=False, choices = (
        ('random', 'Random'), 
        ('fixed', 'Fixed'),
    ))

    # Options for Cookies
    cookies_file = forms.CharField(required=False, max_length=2000, label="Cookies File",
        widget=forms.TextInput(attrs={'placeholder': 'Paste here the content of your cookies file'}))
    persist_cookies = forms.BooleanField(required=False, label="Persist Cookies")
    
    # Options for Captcha
    img_url = forms.CharField(required=False, label="Image URL", max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Image URL'})
    )
    img_xpath = forms.CharField(required=False, label="Image Xpath", max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Image Xpath'})
    )
    sound_url = forms.CharField(required=False, label="Sound URL", max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sound URL'})
    )
    sound_xpath = forms.CharField(required=False, label="Sound Xpath", max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Sound Xpath'})
    )
    
    crawler_type = forms.ChoiceField(required=False, choices = (
        ('static_page', 'Static Page'), 
        ('form_page', 'Page with Form'),
        ('single_file', 'Single File'),
        ('bundle_file', 'Bundle File'),
    ), widget=forms.Select(attrs={'onchange': 'detailCrawlerType();'}))
    explore_links = forms.BooleanField(required=False, label="Explore links")
    link_extractor_max_depht = forms.IntegerField(required=False, label="Link extractor max depth")
    link_extractor_allow = forms.CharField(required=False, max_length=2000, label="Link extractor allow",
        widget=forms.TextInput(attrs={'placeholder': 'Regex for allowing on link extractor'}))