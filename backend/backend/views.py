from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


# Decorator specifies method of response
@api_view(['GET'])
def api_root(request, format=None):
    """Table of contents for API

    :request: browser request on url
    :format: request format
    :returns: returns the table of contents

    """
    return Response({
        'soops': reverse('soops:soop-list', request=request, format=format),
    })
