from asyncio.log import logger
from time import sleep

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models.action import Attack, Defend, Move
from api.models.match import MatchIA
from api.models.zone import Zone
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
        attack_to = int(request.data['attack_to'])
        match_id = request.data['match']

        if attack_from == attack_to:
            return Response(
                {"Fail": "attacker and attacked are the same"},
                status=status.HTTP_400_BAD_REQUEST)

        attacker = MatchIA.objects.get(match_id=match_id, ia=attack_from)
        attacked = MatchIA.objects.get(match_id=match_id, ia_id=attack_to)

        if attacked.where_am_i != attacker.where_am_i:
            return Response(
                {"Fail": "wrong ia-match"}, status=status.HTTP_400_BAD_REQUEST)

        if not attacker.alive or not attacked.alive:
            return Response(
                {"Fail": "someone is dead"},
                status=status.HTTP_401_UNAUTHORIZED)

        data = {
            'attack_to': attack_to,
            'match': match_id,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        sleep(settings.ATTACK_DELAY)
        data['status_info'] = {
            attack_from: {
                'lucky_unlucky': attacker.lucky_unlucky,
                'go_ryu': attacker.go_ryu
            },
            attack_to: {
                'lucky_unlucky': attacked.lucky_unlucky,
                'go_ryu': attacked.go_ryu
            }
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        damage = serializer.validated_data['match'].damage
        attack_from = self.request.user.ia
        serializer.save(damage=damage, attack_from=attack_from)


class MoveViewSet(ModelViewSet):
    serializer_class = MoveSerializer
    queryset = Move.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(ia=self.request.user.ia)

    def create(self, request):
        sleep(settings.MOVE_DELAY)
        ia = request.user.ia.id
        to_zone = request.data['to_zone']
        match_id = request.data['match']

        if not MatchIA.if_ia_in_match(ia, match_id):
            return Response(
                {"Fail": "wrong ia-match"}, status=status.HTTP_400_BAD_REQUEST)

        match_ia_instance = MatchIA.objects.get(match_id=match_id, ia=ia)

        if not match_ia_instance.alive:
            return Response(
                {"Fail": "you are dead"}, status=status.HTTP_401_UNAUTHORIZED)

        zone_instance = Zone.objects.get(id=to_zone)
        if not zone_instance.enable:
            return Response(
                {"Fail": "this zone is disable"},
                status=status.HTTP_401_UNAUTHORIZED)

        data = {
            'to_zone': to_zone,
            'match': match_id,
            'triggers': {
                'lucky_unlucky': zone_instance.lucky_unlucky,
                'go_ryu': zone_instance.go_ryu,
                'karin_gift': zone_instance.karin_gift
            }
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

    def get_queryset(self):
        return Defend.objects.all().filter(match_ia__ia=self.request.user.ia)

    def create(self, request):
        ia = request.user.ia.id
        active = request.data.get('active', False)
        match_ia = request.data['match_ia']

        try:
            match_ia_instance = MatchIA.objects.get(id=match_ia, ia=ia)
        except Exception as e:
            logger.error(e)
            return Response(
                {"Fail": "wrong ia-match"}, status=status.HTTP_400_BAD_REQUEST)

        if not match_ia_instance.alive:
            return Response(
                {"Fail": "you are dead"}, status=status.HTTP_401_UNAUTHORIZED)

        data = {
            'active': active,
            'match_ia': match_ia
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.match_ia.ia == request.user.ia and\
           int(request.data['match_ia']) == instance.match_ia.id and\
           instance.match_ia.alive:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
