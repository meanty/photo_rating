# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from app_userlist.models import Profile
from app_userlist.serializers import UserSerializer
from datetime import datetime
import json
import settings


class ClientsListView (generics.ListAPIView):
    model = Profile
    queryset = Profile.objects.all().order_by('surname')
    serializer_class = UserSerializer


def init(request):
    context_object_name = 'clients'
    queryset = Profile.objects.all().order_by('surname')
    response_data = {
        'clients': queryset,
    }
    return render(request, 'index.html', response_data) 


def search(request):
    if request.method == 'POST':
        search_text = request.POST.get('search', None)
        try:
            if not search_text:
                user = Profile.objects.all().order_by('surname')
            else:
                query = Q(first_name__contains=search_text) | Q(surname__contains=search_text)
                user = Profile.objects.filter(query)
            response_data = {
                'clients': user,
            }
            return render(request, 'index.html', response_data)
        except Profile.DoesNotExist:
            return render(request, 'index.html', {'clients': Profile.objects.all().order_by('surname')})
    else:
        return render(request, 'index.html')


def xlsx (request):
    from django.core.serializers import serialize
    from django.utils.encoding import iri_to_uri
    if request.method == 'POST':
        search_text = request.POST.get('search', None)
        file_name = 'clients_dump_' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        records = Profile.objects.all()
        if records.count()==0:
            return HttpResponse('<h3>No one client yet</h3>')
        else:
            serial_result = serialize('xlsx', records)
            serial_result.seek(0)
            response = HttpResponse(serial_result.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="' + \
                iri_to_uri(file_name) + '.xlsx"'
            return response
    else:
        return render(request, 'index.html')


def create(request):
    context_object_name = 'new_client'
    queryset = Profile.objects.all().order_by('surname')
    response_data = {
        'clients': queryset,
    }
    return render(request, 'index.html', response_data) 

def vote(request, pk):
    person = get_object_or_404(Profile, pk=pk)
    new_rating = person.rating + 1
    setattr(person, 'rating', new_rating)
    print person.rating
    person.save()
    # person.update(rating = str(new_rating))
    queryset = Profile.objects.all().order_by('-rating')
    response_data = {
        'clients': queryset,
    }
    return render(request, 'vote_page.html', response_data) 
    # except:
    #     queryset = Profile.objects.all().order_by('surname')
    #     response_data = {
    #         'clients': queryset,
    #     }
    #     return HttpResponseRedirect ('/', response_data) 


    # def post(self, request, pk, *args, **kwargs):
    #     person = get_object_or_404(Profile, pk=pk)
    #     data = { 'deleted': person }
    #     print '!!!!!!!'
    #     # serializer = VoteSerializer(queryset, many=True)
    #     return Response(data=data)