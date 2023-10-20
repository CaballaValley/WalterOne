from datetime import datetime
import pytz

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404


from api.models.match import Match

ES_TIMEZONE = pytz.timezone('Europe/Madrid')


def info_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    template = loader.get_template("match_zones.html")
    context = {
        "match_name": match.name,
        "refresh": request.GET.get('refresh', 2),
        "datetime": datetime.now(ES_TIMEZONE).isoformat()
    }

    ias = []
    for match_ia in match.matchia_set.order_by("-life"):
        ias.append({
            "name": match_ia.ia.name,
            "id": match_ia.id,
            "zone": match_ia.where_am_i.name,
            "life": match_ia.life,
            "lucky_unlucky": match_ia.lucky_unlucky,
            "go_ryu": match_ia.go_ryu,
        })

    context["match_ias"] = ias

    attacks_limit = request.GET.get("attacks_limit", 15)
    attacks_qs = match.attack_set.order_by("-timestamp")[:attacks_limit]

    attacks = []
    for attack in attacks_qs:
        attacks.append(attack)

    context["attacks"] = attacks
    return HttpResponse(template.render(context, request))


def info(request):
    template = loader.get_template("info.html")

    return HttpResponse(template.render({}, request))
