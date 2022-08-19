from rest_framework.serializers import ModelSerializer, BooleanField

from api.models.action import Attack, Defend, Move


class AttackSerializer(ModelSerializer):
   class Meta:
      model = Attack
      fields = ['match', 'attack_to', 'attack_from', 'timestamp']
      read_only_fields = ['attack_from', 'timestamp']


class MoveSerializer(ModelSerializer):
   class Meta:
      model = Move
      fields = ['match', 'to_zone', 'ia','timestamp']
      read_only_fields = ['ia', 'timestamp']


class DefendSerializer(ModelSerializer):
   active = BooleanField(required=False)
   class Meta:
      model = Defend
      fields = ['match_ia', 'active', 'id']
      read_only_fields = ['id']
