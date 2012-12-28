# -*- coding: utf-8 -*-
# Copyright (c) 2012 Fabian Barkhau <fabian.barkhau@gmail.com>                  
# License: MIT (see LICENSE.TXT file) 


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries import CountryField
from django.core.validators import RegexValidator
from apps.common.shortcuts import HUMAN_LINK_FORMAT as HLF


STATUSES = [
    'PENDING',
    'ACCEPTED',
    'DECLINED',
]
STATUS_CHOICES = [(request, _(request)) for request in STATUSES]


class Team(models.Model):

    link        = models.CharField(max_length=128, unique=True, validators=[RegexValidator('^%s$' % HLF)])
    name        = models.CharField(max_length=1024, unique=True)
    members     = models.ManyToManyField('account.Account', null=True, blank=True) 
    country     = CountryField()

    # meta
    created_by  = models.ForeignKey('account.Account', related_name='team_created')
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey('account.Account', related_name='team_updated')
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:                                                                                                 
                                                                                                                
        ordering = ['name']


class JoinRequest(models.Model):

    # main data
    team        = models.ForeignKey('team.Team', related_name='join_requests') # team user wants to join
    requester   = models.ForeignKey('account.Account', related_name='join_requests_made') # user who is requesting to join
    processor   = models.ForeignKey('account.Account', related_name='join_requests_processed') # user who answerd the request
    status      = models.CharField(max_length=256, choices=STATUS_CHOICES, default='PENDING')
    application = models.TextField() # reason given by user to join
    response    = models.TextField() # reason given by processor

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.team.id, self.requester.id)
        return u"id: %s; team_id: %s; requester_id: %s" % args


class RemoveRequest(models.Model):

    # main data
    team        = models.ForeignKey('team.Team', related_name='remove_requests') # team to remove user from
    concerned   = models.ForeignKey('account.Account', related_name='remove_requests_concerned') # user to be removed
    requester   = models.ForeignKey('account.Account', related_name='remove_requests_made') # user who is requesting the removel
    processor   = models.ForeignKey('account.Account', related_name='remove_requests_processed') # user who processed the request
    status      = models.CharField(max_length=256, choices=STATUS_CHOICES, default='PENDING')
    reason      = models.TextField() # reason given by by the requester
    response    = models.TextField() # reason given by processor

    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.team.id, self.concerned.id)
        return u"id: %s; team_id: %s; concerned_id: %s" % args


class Page(models.Model):

    team        = models.ForeignKey('team.Team', related_name='pages')
    link        = models.CharField(max_length=128, validators=[RegexValidator('^%s$' % HLF)])
    name        = models.CharField(max_length=1024)
    content     = models.TextField() # TODO make wiki or markdown
    order       = models.IntegerField() # TODO allow None

    # meta
    created_by  = models.ForeignKey('account.Account', related_name='pages_created')
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey('account.Account', related_name='pages_updated')
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        return u"%s: %s" % (self.team.name, self.name)

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('team', 'name'), ('team', 'link')) 
        ordering = ['order', 'created_on']


class Blog(models.Model):

    team        = models.ForeignKey('team.Team', related_name='blogs')
    name        = models.CharField(max_length=1024)
    content     = models.TextField() # TODO make wiki or markdown

    # meta
    created_by  = models.ForeignKey('account.Account', related_name='blogs_created')
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_by  = models.ForeignKey('account.Account', related_name='blogs_updated')
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        return u"%s: %s" % (self.team.name, self.name)

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('team', 'name')) 
        ordering = ['created_on']


class Station(models.Model):

    owner       = models.ForeignKey('account.Account')
    preview     = models.ForeignKey('image.Image', related_name='station_previews', blank=True, null=True)
    capacity    = models.IntegerField(default=1)
    active      = models.BooleanField(default=True)
    street      = models.CharField(max_length=1024)
    city        = models.CharField(max_length=1024)
    postalcode  = models.CharField(max_length=1024)
    country     = CountryField()
    # TODO link on google maps 
    
    # meta
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    # TODO validation

    def __unicode__(self):
        args = (self.id, self.owner.id, self.street, self.postalcode, self.city, self.country)
        return u"id: %s; owner_id: %s; %s, %s, %s, %s" % args

    class Meta:                                                                                                 
                                                                                                                
        unique_together = (('owner', 'street', 'city', 'postalcode', 'country'),) 

