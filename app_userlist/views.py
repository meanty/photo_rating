# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.decorators import list_route#, api_view
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
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
        return Response(data=request.POST, status=status.HTTP_200_OK, template_name='create_user.html')


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return super(UserCreateView, self).post(request, *args, **kwargs)


class VotePage(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    context_object_name = 'clients'

    def get(self, request, format=None):
        queryset = Profile.objects.all().order_by('-rating')
        serializer = VoteSerializer(queryset, many=True)
        return Response(data={'clients': serializer.data}, status=status.HTTP_200_OK, template_name='vote_page.html')

    def post(self, request, *args, **kwargs):
        queryset = Profile.objects.all().order_by('-rating')
        serializer = VoteSerializer(queryset, many=True)
        return Response(data={'clients': serializer.data}, status=status.HTTP_200_OK, template_name='vote_page.html')


# class CreateClientSet(viewsets.ModelViewSet):
#     # renderer_classes = (TemplateHTMLRenderer,)
#     queryset = Profile.objects.all()
#     serializer_class = VoteSerializer

#     # @list_route(methods=['post', 'get'])
#     def get_serializer_context(self):
#         """
#         Adds a new client
#         """
#         user = request.user
#         context = super().get_serializer_context()
#         return {'request': self.request, 'view': self}
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
        vote_rating = Profile.objects.all().order_by('-rating')
        # vote_param = request.query_params.get("rating", None)
        page = self.paginate_queryset(vote_rating)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(vote_rating, many=True)
        # return Response({'clients': serializer.data}, template_name='vote_page.html')
        return Response(serializer.data)


def user_create(request):
    client_name = request.POST.get('first_name') if request.POST.get('first_name') else 'Name'
    client_surname = request.POST.get('surname') if request.POST.get('surname') else 'Surname'
    date = request.POST.get('birthday') if request.POST.get('birthday') else None
    photo = request.FILES.get('file') if request.FILES.get('file') else None
    Profile.objects.create(
        first_name=client_name, 
        surname=client_surname, 
        birthday=date, 
        photo=photo, 
        rating=0,
    )
    user = Profile.objects.all()
    return HttpResponseRedirect('/', {'clients': user})