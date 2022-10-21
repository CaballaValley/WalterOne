import logging

from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


from api.models.match import MatchIA
from api.models.zone import Zone


class FindViewSet(ViewSet):
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
            match_ias = MatchIA.objects.filter(
                match_id=match,
                where_am_i_id=self_match_ia.where_am_i.id,
                alive=True
            )
            neighbours_zones = self_match_ia.where_am_i.neighbors.all()
            logging.info(
                "*"*20,
                self.request.user.ia,
                self_match_ia.where_am_i,
                [ia.id for ia in match_ias]
            )
        else:
            match_ias = MatchIA.objects.none()
            neighbours_zones = Zone.objects.none()

        ias = []
        for match_ia in match_ias:
            if match_ia.ia.id != self.request.user.ia.id and match_ia.alive:
                ias.append(match_ia.ia.id)

        neighbours_zones_ids = []
        for zone in neighbours_zones:
            if zone.enable:
                neighbours_zones_ids.append(zone.id)

        return Response({
            'ias': ias,
            'neighbours_zones': neighbours_zones_ids,
            'triggers': {
                'lucky_unlucky': match_ia.where_am_i.lucky_unlucky,
                'go_ryu': match_ia.where_am_i.go_ryu,
                'karin_gift': match_ia.where_am_i.karin_gift
            },
            'life': self_match_ia.life,
        })
