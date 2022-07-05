from rest_framework.viewsets import ModelViewSet

from api.models.action import Attack
from api.serializers.actions import AttackSerializer

class AttackViewSet(ModelViewSet):
    serializer_class = AttackSerializer
    queryset = Attack.objects.all()