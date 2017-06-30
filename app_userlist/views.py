# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins, status
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from serializers import *
from models import *


class UserCard(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, pk, format=None):
        person = get_object_or_404(Profile, pk=pk)
        serializer = UserSerializer(person)
        return Response(data=serializer.data, status=status.HTTP_200_OK, template_name='user_card.html')

    # def delete(self, request, pk, format=None):
        # print request.method
        # print 'DEL'
        # person = get_object_or_404(Profile, pk=pk)
        # person.destroy(request, *args, **kwargs)
        # return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk, format=None): # Delete!
        person = get_object_or_404(Profile, pk=pk)
        data = { 'deleted': person }
        person.delete()
        return Response(data=data, status=status.HTTP_200_OK, template_name='delete_user.html')



class CreateFormView(generics.CreateAPIView):
    renderer_classes = (TemplateHTMLRenderer,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs): # Create!
        print '00000'
        data = request.POST
        print data
        return Response(data=data, status=status.HTTP_200_OK, template_name='create_user.html')


class UserCreateView(generics.CreateAPIView):
    # renderer_classes = (TemplateHTMLRenderer,)                             
    # queryset = Profile.objects.all()
    serializer_class = UserSerializer
    # model = Profile

    def post(self, request, *args, **kwargs):
        print '+++++++++ request +++++++++', dir(request)
        return super(UserCreateView, self).post(request, *args, **kwargs)


class VotePage(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    context_object_name = 'clients'

    def get(self, request, format=None):
        print 'GET'
        queryset = Profile.objects.all().order_by('-rating')
        serializer = VoteSerializer(queryset, many=True)
        return Response(data={'clients': serializer.data}, status=status.HTTP_200_OK, template_name='vote_page.html')

    def post(self, request, *args, **kwargs):
        print 'POST'
        queryset = Profile.objects.all().order_by('-rating')
        serializer = VoteSerializer(queryset, many=True)
        print serializer.data
        return Response(data={'clients': serializer.data}, status=status.HTTP_200_OK, template_name='vote_page.html')


class CreateClientSet(viewsets.ModelViewSet):
    # renderer_classes = (TemplateHTMLRenderer,)
    queryset = Profile.objects.all()
    serializer_class = VoteSerializer

    # @list_route(methods=['post', 'get'])
    def get_serializer_context(self):
        """
        Adds a new client
        """
        user = request.user
        # print 'QQQQQ', request
        print ' ---- ', self.request
        context = super().get_serializer_context()
        context['foo'] = 'bar'
        return {'request': self.request, 'view': self}
        # return Response(serializer.data)





class VoteSet(viewsets.ModelViewSet):
    # renderer_classes = (TemplateHTMLRenderer,)
    queryset = Profile.objects.all()
    serializer_class = VoteSerializer

    @list_route(methods=['post', 'get'])
    def all(self, request):
        """
        Adds a new vote to the object.
        """
        user = request.user
        print 'QQQQQ', request.query_params
        vote_rating = Profile.objects.all().order_by('-rating')
        vote_param = request.query_params.get("rating", None)
        vote_dict = {"true": True,
                     "false": False}
        page = self.paginate_queryset(vote_rating)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(vote_rating, many=True)
        # return Response({'clients': serializer.data}, template_name='vote_page.html')
        return Response(serializer.data)
        # try:
        #     vote = vote_dict[vote_param]
        #     model = request.query_params.get("model", None)
        #     id = request.query_params.get("id", None)

        #     content_type = ContentType.objects.get(model=model)
        #     instance = content_type.get_object_for_this_type(pk=id)
        #     instance.votes.up(user, vote)
        #     message = "Successfully voted"

        # except KeyError:
        #     message = "Please provide a like or dislike parameter."
        # return Response(data=message, status=status.HTTP_200_OK, template_name='vote_page.html')



def user_create(request):
    print request.FILES
    print dir(request)
    client_name = request.POST.get('first_name') if request.POST.get('first_name') else 'Name'
    client_surname = request.POST.get('surname') if request.POST.get('surname') else 'Surname'
    date = request.POST.get('birthday') if request.POST.get('birthday') else None
    photo = request.FILES.get('file') if request.FILES.get('file') else None
    print client_name, client_surname, date, photo
    Profile.objects.create(
        first_name=client_name, 
        surname=client_surname, 
        birthday=date, 
        photo=photo, 
        rating=0,
    )

    print 'create'
    user = Profile.objects.all()
    print user
    return HttpResponseRedirect('/', {'clients': user})