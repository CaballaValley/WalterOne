from datetime import datetime
import pytz

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404


from api.models.match import Match
from api.models.action import FinalDamage

ES_TIMEZONE = pytz.timezone('Europe/Madrid')


def info_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    template = loader.get_template("info_match.html")
    context = {
        "match_name": match.name,
        "refresh": request.GET.get('refresh', 2),
        "datetime": datetime.now(ES_TIMEZONE).isoformat()
    }

    context["match_ias"] = [
        match_ia for match_ia in match.matchia_set.order_by("-life")]

    attacks_limit = request.GET.get("attacks_limit", 11)
    context["attacks"] = [
        attack for attack in FinalDamage.objects.filter(match_id=match_id).order_by("-timestamp")[:attacks_limit]]

    return HttpResponse(template.render(context, request))


def info(request):
    template = loader.get_template("info.html")

    return HttpResponse(template.render({}, request))
