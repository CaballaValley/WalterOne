from rest_framework.serializers import ModelSerializer

from api.models.action import Attack

class AttackSerializer(ModelSerializer):
   class Meta:
      model = Attack
      fields = ['match_ia', 'attack_to']
