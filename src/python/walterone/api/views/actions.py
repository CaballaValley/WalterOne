from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models.action import Attack
from api.models.ia import IA
from api.models.match import Match
from api.serializers.actions import AttackSerializer

class AttackViewSet(ModelViewSet):
    serializer_class = AttackSerializer
    queryset = Attack.objects.all()

    def get_queryset(self):                                          
        return super().get_queryset().filter(attack_from=self.request.user.ia) 
    
    def create(self, request):
        attack_from = request.user.ia.id
        attack_to = request.data['attack_to']

        if attack_from == attack_to:
            return Response({"Fail": "attacker and attacked are the same"}, status=status.HTTP_400_BAD_REQUEST)

        match = Match.objects.get(id=request.data['match'])
        data = {
            'attack_to': attack_to,
            'attack_from': attack_from,
            'match': match.id,
            'damage': match.damage
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)