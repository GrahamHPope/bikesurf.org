# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db.models import Model
from django.db.models import ForeignKey
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import TextField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import URLField
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def signed_up_callback(sender, **kwargs):
    account = Account()
    account.user = kwargs["user"]
    account.save()


class Account(Model):

    SOURCES_CHOICES = [
        ('OTHER', _('OTHER')),
        ('COUCHSURFING', _('COUCHSURFING')),
        ('FACEBOOK', _('FACEBOOK')),
        ('FRIENDS', _('FRIENDS')),
        ('GOOGLE', _('GOOGLE')),
        ('TWITTER', _('TWITTER')),
    ]

    # main data
    user = ForeignKey('auth.User', unique=True, related_name="accounts")
    description = TextField(blank=True)
    source = CharField(max_length=64, choices=SOURCES_CHOICES, default='OTHER')
    feedback = TextField(blank=True)
    mobile = CharField(max_length=1024, blank=True)

    # meta
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    # TODO validation

    def get_name():
        return self.user.username

    def __unicode__(self):
        return self.user.username

    class Meta:

        ordering = ['user__username']


class Site(Model):

    SITE_CHOICES = [ # TODO add url validation functions per site
        ('COUCHSURFING', _('COUCHSURFING')),
        ('FACEBOOK', _('FACEBOOK')),
        ('TWITTER', _('TWITTER')),
        ('GOOGLEPLUS', _('GOOGLEPLUS')),
        ('BLOG', _('BLOG')),
        ('SKYPE', _('SKYPE')),
        ('LINKED_IN', _('LINKED_IN')),
        ('BE_WELCOME', _('BE_WELCOME')),
        ('WARM_SHOWERS', _('WARM_SHOWERS')),
        ('PINTEREST', _('PINTEREST')),
        ('YOUTUBE', _('YOUTUBE')),
    ]

    # main data
    account = ForeignKey('account.Account')
    site = CharField(max_length=64, choices=SITE_CHOICES)
    link = URLField()
    confirmed = BooleanField(default=False) # done by bike lender

    # meta
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    def __unicode__(self):
        args = (self.id, self.account.id, self.site, self.confirmed)
        return u"id: %s; account_id: %s; site: %s; confirmed: %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('account', 'site'),) 


class Vacation(Model):

    account = ForeignKey('account.Account')
    start = DateField()
    finish = DateField() # inclusive

    # meta
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.user.id, self.start, self.finish)
        return u"id: %s; user_id: %s; start: %s; finish: %s" % args
    



