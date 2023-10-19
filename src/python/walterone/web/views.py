from datetime import datetime
import pytz

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404


from api.models.match import Match

ES_TIMEZONE = pytz.timezone('Europe/Madrid')


def zones(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    template = loader.get_template("match_zones.html")
    context = {
        "match_name": match.name,
        "refresh": request.GET.get('refresh', 5),
        "datetime": datetime.now(ES_TIMEZONE).isoformat()
    }

    zones_elements = []
    for i, zone in enumerate(match.map.zone_set.all(), 1):
        n_neighbors = zone.neighbors.count()
        neighbors = [
            z.name
            for z in zone.neighbors.all()
        ]
        zone_element = {
            "status": "enabled" if zone.enable else "dissabled",
            "name": zone.name,
            "id": zone.id,
            "number_neighbours": n_neighbors,
            "vecinos": ", ".join(neighbors),
            "lucky_unlucky": zone.lucky_unlucky,
            "karin_gift": zone.karin_gift,
            "go_ryu": zone.go_ryu,
        }
        zones_elements.append(zone_element)

    context["zones"] = zones_elements

    ias = []
    for match_ia in match.matchia_set.order_by("-life"):
        print(match_ia)
        ias.append({
            "name": match_ia.ia.name,
            "id": match_ia.id,
            "zone": match_ia.where_am_i.name,
            "life": match_ia.life,
            "lucky_unlucky": match_ia.lucky_unlucky,
            "go_ryu": match_ia.go_ryu,
        })

    context["match_ias"] = ias

    return HttpResponse(template.render(context, request))


def info(request):
    template = loader.get_template("info.html")

    return HttpResponse(template.render({}, request))
