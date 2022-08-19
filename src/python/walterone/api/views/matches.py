from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ReadOnlyModelViewSet


from api.serializers.matches import FindSerializer
from api.models.match import MatchIA


class FindViewSet(ReadOnlyModelViewSet):
    serializer_class = FindSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['where_am_i', 'match']

    def get_queryset(self):
        match = self.request.query_params.get('match')
        where_am_i = self.request.query_params.get('where_am_i')
        if match and where_am_i:
            if not self.request.user.ia.matchia_set.filter(where_am_i=where_am_i):
                raise ValidationError(
                    f"You are not in this zone {where_am_i}"
                )
            ias = MatchIA.objects.filter(match=match, where_am_i=where_am_i)
        else:
            ias = MatchIA.objects.none()
        return ias