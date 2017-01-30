from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.utils import timezone

"""
class User(AbstractBaseUser):
    "\"\"
    Custom user class.
    "\"\"
    username = models.CharField('username', unique=True,
                                db_index=True, max_length=25)
    email = models.EmailField('email address', unique=True)
        
    joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username
"""

class GHedListManager(models.Manager):
    def get_queryset(self):
        return super(GHedListManager,
                     self).get_queryset().filter(
                         matched=True, PHed = True,
                         deactivated=False)

class PHedListManager(models.Manager):
    def get_queryset(self):
        return super(PHedListManager,
                     self).get_queryset().filter(
                         matched=False, PHed = False,
                         deactivated=False)
    
class Profile(models.Model):
    """
    Profile model
    """
    PACKAGE_CHOICES = (
        ('None', 'None'),
        ('5k', '5k'),
        ('10k', '10k'),
        ('15k', '15k'),
        ('20k', '20k'),
        ('50k', '50k'),
        ('100k', '100k'),
        ('200k', '200k'),
        ('500k', '500k'),
        )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    phone = models.CharField(max_length=11)
    bank = models.CharField(max_length=50)
    account_number = models.CharField(max_length=10)

    init_time = models.CharField(max_length=50, default="0")
    matched = models.BooleanField(default=False)
    package = models.CharField(max_length=4,
                              choices=PACKAGE_CHOICES, default='None')
    PH_time = models.DateTimeField(default=timezone.now)
    PHed = models.BooleanField(default=False)
    deactivated = models.BooleanField(default=False)
    no_of_payers = models.IntegerField(default=0)
    no_of_paid = models.IntegerField(default=0)
    upliner = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       blank=True, related_name='upliner')
    downliner = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       blank=True, related_name='downliner')

    objects = models.Manager() # The default manager.
    
    # Our custom manager.
    GH_list = GHedListManager() 
    PH_list = PHedListManager()

    class Meta:
        ordering = ('-PH_time',)

""" 
class UserFollowers(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=0)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       blank=True, related_name='followers')
    
    def __unicode__(self):
        return '%s, %s' % (self.user, self.count)
"""




