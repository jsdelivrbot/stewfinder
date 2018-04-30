from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from soops.serializers import SoopSerializer
from soops.models import Soop

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
