from django.db import models

# Create your models here.

class CrawlRequest(models.Model):
    source_name = models.CharField(max_length=200)
    base_url  = models.CharField(max_length=200)
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
        ('1', 'None'), 
        ('2', 'Image'),
        ('3', 'Sound'),
    ]

    antiblock = models.CharField(max_length=15, choices=ANTIBLOCK_TYPE, default='none')
    
    # Options for antiblock
        # Options for IP rotation
    ip_type = models.CharField(max_length=15, choices=IP_TYPE, null=True, blank=True)
    tor_password = models.CharField(max_length=20, blank=True) # available for Tor
    proxy_list = models.FileField(max_length=20, blank=True, upload_to=None) # available for Proxy List
    max_reqs_per_ip = models.IntegerField(blank=True)
    max_reuse_rounds = models.IntegerField(blank=True)

        # Options for User Agent rotation 
    reqs_per_user_agent = models.IntegerField(blank=True)
    user_agents_file = models.FileField(max_length=20, blank=True, upload_to=None) # available for Proxy List
    
        # Options for Delay
    delay_secs = models.IntegerField(blank=True)

    captcha = models.CharField(max_length=15, choices=CAPTCHA_TYPE, default='1')
    # steps = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.source_name