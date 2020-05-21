from django.db import models

# Create your models here.

class CrawlRequest(models.Model):
    source_name = models.CharField(max_length=200)
    base_url  = models.CharField(max_length=200)
    # ANTIBLOCK_TYPE = [
    #     ('1', 'None'),
    #     ('2', 'IP rotation'),
    #     ('3', 'User-agent rotation'),
    #     ('4', 'Random delays'),
    #     ('5', 'Use proxy'),
    #     ('6', 'Use cookies'),
    # ]

    CAPTCHA_TYPE = [
        ('1', 'None'), 
        ('2', 'Image'),
        ('3', 'Sound'),
    ]

    # antiblock = models.CharField(max_length=15, choices=ANTIBLOCK_TYPE, default='1')
    captcha = models.CharField(max_length=15, choices=CAPTCHA_TYPE, default='1')

    def __str__(self):
        return self.source_name