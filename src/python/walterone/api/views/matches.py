from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models.match import MatchIA
from api.models.zone import Zone


class FindViewSet(ViewSet):
    def retrieve(self, request):
        match = request.query_params.get('match')
        if match:
            match_ia = MatchIA.objects.get(
                match_id=match,
                ia_id=self.request.user.ia.id,
                alive=True
            )
            ias = MatchIA.objects.filter(
                match_id=match,
                where_am_i_id=match_ia.where_am_i.id,
                alive=True
            )
            neighbours_zones = match_ia.where_am_i.neighbors.all()
            print(
                "*"*20,
                self.request.user.ia,
                match_ia.where_am_i,
                [ia.id for ia in ias]
            )
        else:
            ias = MatchIA.objects.none()
            neighbours_zones = Zone.objects.none()
        return Response({
            'ias': [ia.id for ia in ias],
            'neighbours_zones': [zone.id for zone in neighbours_zones]
        })
