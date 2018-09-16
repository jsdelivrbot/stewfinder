import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from soops.models import Soop
from soops.serializers import SoopSerializer

# Create your views here.


class SoopList(generics.ListCreateAPIView):
    """Create a soop item"""
    queryset = Soop.objects.all()
    serializer_class = SoopSerializer

    def perform_create(self, serializer):
        """Creates a soop item

        :serializer: TODO
        :returns: TODO

        """
        serializer.save()


class SoopDetail(generics.RetrieveUpdateDestroyAPIView):

    """Do anything other than create a soop item"""

    serializer_class = SoopSerializer

    def get_queryset(self):
        """override the get_queryset method
        :returns: TODO

        """

        return Soop.objects.all().filter()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def GetNumVotes(request, soop_id):
    """return the votes for a given soup id

    :soop_id: id of the object
    :returns: integer number of total votes

    """
    obj = Soop.objects.get(pk=soop_id)

    return HttpResponse(obj.votes.count())


def VoteUp(request, soop_id):
    """return the votes for a given soup id

    :soop_id: id of the object
    :returns: integer number of total votes

    """
    obj = Soop.objects.get(pk=soop_id)
    user_id = request.user.id

    ip = get_client_ip(request)
    ip_int = int(ip.replace('.', ''))

    return HttpResponse(obj.votes.up(ip_int))


def VoteDown(request, soop_id):
    """return the votes for a given soup id

    :soop_id: id of the object
    :returns: integer number of total votes

    """
    obj = Soop.objects.get(pk=soop_id)
    user_id = request.user.id

    ip = get_client_ip(request)
    ip_int = int(ip.replace('.', ''))

    return HttpResponse(obj.votes.down(ip_int))


def UserVotes(request, soop_id):
    """return the votes for a given soup id

    :soop_id: id of the object
    :returns: integer number of total votes

    """
    obj = Soop.objects.get(pk=soop_id)

    ip = get_client_ip(request)
    ip_int = int(ip.replace('.', ''))

    results = list(obj.votes.all(ip_int).values())
    return JsonResponse(results, safe=False)


def VoteDelete(request, soop_id):
    """return the votes for a given soup id

    :soop_id: id of the object
    :returns: integer number of total votes

    """
    obj = Soop.objects.get(pk=soop_id)

    ip = get_client_ip(request)
    ip_int = int(ip.replace('.', ''))

    return HttpResponse(obj.votes.delete(ip_int))
