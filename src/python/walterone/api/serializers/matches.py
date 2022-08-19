from rest_framework.serializers import ModelSerializer

from api.models.match import MatchIA


class FindSerializer(ModelSerializer):
   class Meta:
      model = MatchIA
      fields = ['match', 'where_am_i', 'ia']



