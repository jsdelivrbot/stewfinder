from rest_framework import serializers

from soops.models import Soop

class SoopSerializer(serializers.HyperlinkedModelSerializer):

    """turns the python data into JSON and the JSON into python data"""

    class Meta:
        model = Soop

        fields = [
            'url', 
            'id', 
            'created',
            'title',
            'details',
            'day',
            'outUrl',
            'food',
            'when',
            'location'
        ]

        extra_kwargs = {
            'url': {
                'view_name': 'soops:soop-detail',
            }
        }
