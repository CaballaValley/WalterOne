import logging

from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


from api.models.match import MatchIA
from api.models.zone import Zone


class FindViewSet(ViewSet):
    def get_info_zone(self, match, zone):
        match_ias = MatchIA.objects.filter(
                match_id=match,
                where_am_i=zone,
                alive=True
            )
        return {
            "zone_id": zone.id,
            "enable": zone.enable,
            "ias": [
                {
                    "id": match_ia.ia.id,
                    "life": match_ia.life,
                    "role": match_ia.ia.role,
                    'buff': {
                        "go_ryu": match_ia.go_ryu,
                        "lucky_unlucky": match_ia.lucky_unlucky
                    }
                } for match_ia in match_ias
                if match_ia.ia.id != self.request.user.ia.id
            ],
            "triggers": {
                'lucky_unlucky': zone.lucky_unlucky,
                'go_ryu': zone.go_ryu,
                'karin_gift': zone.karin_gift
            }
        }

    def retrieve(self, request):
        match = request.query_params.get('match')
        if match:
            try:
                self_match_ia = MatchIA.objects.get(
                    match_id=match,
                    ia_id=self.request.user.ia.id
                )
            except Exception as e:
                msg = f"User {self.request.user.ia.id} is not in match {match} {e}"
                logging.error(msg)
                raise PermissionDenied(msg)

            if self_match_ia.alive:
                match_ias = MatchIA.objects.filter(
                    match_id=match,
                    where_am_i_id=self_match_ia.where_am_i.id,
                    alive=True
                )
                neighbours_zones = self_match_ia.where_am_i.neighbors.filter(enable=True)
                logging.info(
                    "*"*20,
                    self.request.user.ia,
                    self_match_ia.where_am_i,
                    [ia.id for ia in match_ias]
                )
            else:
                msg = f"User {self.request.user.ia.id} is dead in match {match}"
                logging.error(msg)
                raise PermissionDenied(msg)
        else:
            neighbours_zones = Zone.objects.none()

        return Response({
            "current_zone": self.get_info_zone(
                match, self_match_ia.where_am_i),
            'neighbours_zones': [ 
                self.get_info_zone(match, zone) for zone in neighbours_zones
            ],
            'status': {
                'buff': {
                    "go_ryu": self_match_ia.go_ryu,
                    "lucky_unlucky": self_match_ia.lucky_unlucky
                },
                'life': self_match_ia.life,
                'match_ia': self_match_ia.id,
                'role': self_match_ia.ia.role
            }
        })
