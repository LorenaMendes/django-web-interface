from django.db import models
from django.utils import timezone

class TimeStamped(models.Model):
    creation_date = models.DateTimeField()
    last_modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()

        self.last_modified = timezone.now()
        return super(TimeStamped, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class CrawlRequest(TimeStamped):
    running = models.BooleanField(default=False)
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
    antiblock = models.CharField(max_length=15, choices=ANTIBLOCK_TYPE, default='none')
    
    # Options for antiblock
        # Options for IP rotation
    IP_TYPE = [
        ('tor', 'Tor'),
        ('proxy', 'Proxy'),
    ]
    ip_type = models.CharField(max_length=15, choices=IP_TYPE, null=True, blank=True)
    proxy_list = models.CharField(max_length=2000, blank=True, null=True) # available for Proxy List
    max_reqs_per_ip = models.IntegerField(blank=True, null=True)
    max_reuse_rounds = models.IntegerField(blank=True, null=True)

        # Options for User Agent rotation 
    reqs_per_user_agent = models.IntegerField(blank=True, null=True)
    user_agents_file = models.CharField(max_length=2000, blank=True, null=True)
    
        # Options for Delay
    delay_secs = models.IntegerField(blank=True, null=True)

    DELAY_TYPE = [
        ('random', 'Random'), 
        ('fixed', 'Fixed'),
    ]
    delay_type = models.CharField(max_length=15, choices=DELAY_TYPE, blank=True, null=True)
        
        # Options for Cookies
    cookies_file = models.CharField(max_length=2000, blank=True, null=True)
    persist_cookies = models.BooleanField(blank=True, null=True)

    CAPTCHA_TYPE = [
        ('none', 'None'), 
        ('image', 'Image'),
        ('sound', 'Sound'),
    ]
    captcha = models.CharField(max_length=15, choices=CAPTCHA_TYPE, default='none')
    has_webdriver = models.BooleanField(blank=True, null=True)
    webdriver_path = models.CharField(max_length=1000, blank=True, null=True)
    # Options for captcha
        # Options for image
    img_xpath = models.CharField(max_length=100, blank=True, null=True)
        # Options for sound
    sound_xpath = models.CharField(max_length=100, blank=True, null=True)

    CRAWLER_TYPE = [
        ('static_page', 'Static Page'), 
        ('form_page', 'Page with Form'),
        ('single_file', 'Single File'),
        ('bundle_file', 'Bundle File'),
    ]
    crawler_type = models.CharField(max_length=15, choices=CRAWLER_TYPE, default='static_page')
    explore_links = models.BooleanField(blank=True, null=True)
    link_extractor_max_depht = models.IntegerField(blank=True, null=True)
    link_extractor_allow = models.CharField(max_length=1000, blank=True, null=True)
    link_extractor_allow_extensions = models.CharField(blank=True, null=True, max_length=2000)

    def __str__(self):
        return self.source_name

class CrawlerInstance(TimeStamped):
    crawler_id = models.ForeignKey(CrawlRequest, on_delete=models.CASCADE)
    instance_id = models.BigIntegerField(primary_key=True)
    running = models.BooleanField()
