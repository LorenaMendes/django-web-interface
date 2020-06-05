from django.db import models

# Create your models here.

class CrawlRequest(models.Model):
    source_name = models.CharField(max_length=200)
    base_url  = models.CharField(max_length=200)
    obey_robots = models.BooleanField(blank=True, null=True)
    ANTIBLOCK_TYPE = [
        ('none', 'None'),
        ('ip', 'IP rotation'),
        ('user_agent', 'User-agent rotation'),
        ('delay', 'Delays'),
        ('cookies', 'Use cookies'),
    ]
    
    IP_TYPE = [
        ('tor', 'Tor'),
        ('proxy', 'Proxy'),
    ]
    
    CAPTCHA_TYPE = [
        ('none', 'None'), 
        ('image', 'Image'),
        ('sound', 'Sound'),
    ]

    DELAY_TYPE = [
        ('random', 'Random'), 
        ('fixed', 'Fixed'),
    ]

    antiblock = models.CharField(max_length=15, choices=ANTIBLOCK_TYPE, default='none')
    
    # Options for antiblock
        # Options for IP rotation
    ip_type = models.CharField(max_length=15, choices=IP_TYPE, null=True, blank=True)
    tor_password = models.CharField(max_length=20, blank=True, null=True) # available for Tor
    proxy_list = models.FileField(max_length=20, blank=True, null=True, upload_to=None) # available for Proxy List
    max_reqs_per_ip = models.IntegerField(blank=True, null=True)
    max_reuse_rounds = models.IntegerField(blank=True, null=True)

        # Options for User Agent rotation 
    reqs_per_user_agent = models.IntegerField(blank=True, null=True)
    user_agents_file = models.FileField(max_length=20, blank=True, upload_to=None)
    
        # Options for Delay
    delay_secs = models.IntegerField(blank=True, null=True)
    delay_type = models.CharField(max_length=15, choices=DELAY_TYPE, null=True, blank=True)
        
        # Options for Cookies
    cookies_file = models.FileField(max_length=20, blank=True, null=True, upload_to=None)
    persist_cookies = models.BooleanField(blank=True, null=True)

    captcha = models.CharField(max_length=15, choices=CAPTCHA_TYPE, default='1')

    # Options for captcha
        # Options for image
    img_xpath = models.CharField(max_length=100, blank=True, null=True)
    img_url = models.CharField(max_length=100, blank=True, null=True)
        # Options for sound
    sound_xpath = models.CharField(max_length=100, blank=True, null=True)
    sound_url = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.source_name