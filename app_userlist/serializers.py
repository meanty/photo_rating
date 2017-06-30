# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.db import transaction
from models import Profile
from testpr import settings


class UserSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField(source='calc_age')

    class Meta:
        model = Profile
        fields = ('first_name', 'surname', 'age', 'birthday', 'photo')


class VoteSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        avatar = obj.photo if obj.photo else 'No photo'
        return {
            'name': '{} {}'.format(obj.first_name, obj.surname),
            'photo': avatar,
            'rating': obj.rating,
            'id': obj.id
        }

    @transaction.atomic
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'surname', 'photo', 'rating')
