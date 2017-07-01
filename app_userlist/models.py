# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from datetime import date


class Profile (models.Model):
    first_name = models.CharField(max_length=100, default='Name')
    surname = models.CharField(max_length=100, default='Surname')
    birthday = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='photos', default='photos/anonym.jpg')
    rating = models.DecimalField(null=False, max_digits=2, decimal_places=0, default=0)

    class Meta:
        ordering = ['surname']

    # @property
    def calc_age(self):
        if self.birthday and self.birthday > date.today(): 
            return 'Not yet born 0_o'
        elif self.birthday:
            today = date.today()
            age = today.year - self.birthday.year
            if today.month < self.birthday.month:
                age -= 1
            elif today.month == self.birthday.month and today.day < self.birthday.day:
                age -= 1
            return age
        else:
            return 'Please set birth date'


    def __str__(self):
        return '{} {}'.format(self.first_name, self.surname)

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.surname)


@receiver(pre_save, sender=Profile)
def add_vote(instance, **kwargs):
    try:
        pre_instance = Profile.objects.get(pk=instance.pk)
        if pre_instance.rating > 9:
            instance.rating = 9
            return { 'message': 'rates for maximum' }
    except:
        return { 'message': 'create new instance' }