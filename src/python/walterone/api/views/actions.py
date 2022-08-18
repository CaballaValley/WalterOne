from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models.action import Attack, Defend, Move
from api.models.match import Match, MatchIA
from api.serializers.actions import \
    AttackSerializer,\
    DefendSerializer,\
    MoveSerializer

class AttackViewSet(ModelViewSet):
    serializer_class = AttackSerializer
    queryset = Attack.objects.all()

    def get_queryset(self):                                          
        return super().get_queryset().filter(attack_from=self.request.user.ia) 
    
    def create(self, request):
        attack_from = request.user.ia.id
        attack_to = request.data['attack_to']
        match_id = request.data['match']

        if attack_from == attack_to:
            return Response({"Fail": "attacker and attacked are the same"}, status=status.HTTP_400_BAD_REQUEST)

        if not (MatchIA.if_ia_in_match(attack_from, match_id) and MatchIA.if_ia_in_match(attack_to, match_id)):
            return Response({"Fail": "wrong ia-match"}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'attack_to': attack_to,
            'match': match_id,            
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        damage =  serializer.validated_data['match'].damage
        attack_from = self.request.user.ia
        serializer.save(damage=damage, attack_from=attack_from)


class MoveViewSet(ModelViewSet):
    serializer_class = MoveSerializer
    queryset = Move.objects.all()
    

    def get_queryset(self):                                          
        return super().get_queryset().filter(ia=self.request.user.ia)
    
    def create(self, request):
        ia = request.user.ia.id
        to_zone = request.data['to_zone']
        match_id = request.data['match']

        if not MatchIA.if_ia_in_match(ia, match_id):
            return Response({"Fail": "wrong ia-match"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'to_zone': to_zone,
            'match': match_id
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        ia = self.request.user.ia
        serializer.save(ia=ia)
    
class DefendViewSet(ModelViewSet):
    serializer_class = DefendSerializer
    queryset = Defend.objects.all()

    def get_queryset(self):                                          
        return super().get_queryset().filter(ia=self.request.user.ia)
    
    def create(self, request):
        ia = request.user.ia.id
        active = request.data.get('active', False)
        match_id = request.data['match']

        if not MatchIA.if_ia_in_match(ia, match_id):
            return Response({"Fail": "wrong ia-match"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'active': active,
            'match': match_id
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        ia = self.request.user.ia
        serializer.save(ia=ia)