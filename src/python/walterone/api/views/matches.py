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
            "zone": zone.id,
            "ias": [
                {
                    "id": match_ia.ia.id,
                    "life": match_ia.life
                } for match_ia in match_ias
                if match_ia.ia.id != self.request.user.ia.id
            ],
            'lucky_unlucky': zone.lucky_unlucky,
            'go_ryu': zone.go_ryu,
            'karin_gift': zone.karin_gift
        }

    def retrieve(self, request):
        match = request.query_params.get('match')
        if match:
            try:
                self_match_ia = MatchIA.objects.get(
                    match_id=match,
                    ia_id=self.request.user.ia.id,
                    alive=True
                )
            except Exception as e:
                logging.error(f"Permission denied {e}")
                raise PermissionDenied("You are not alive here!!!")
            neighbours_zones = self_match_ia.where_am_i.neighbors.all()
            logging.info(
                "*"*20,
                self.request.user.ia,
                self_match_ia.where_am_i
            )
        else:
            neighbours_zones = Zone.objects.none()

        return Response({
            "zone": self.get_info_zone(match, self_match_ia.where_am_i),
            'neighbours_zones': [ 
                self.get_info_zone(match, zone) for zone in neighbours_zones
                if zone.enable
            ],
            'life': self_match_ia.life,
        })
