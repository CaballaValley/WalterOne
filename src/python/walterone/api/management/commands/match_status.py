import datetime
from time import sleep
import os
from django.core.management.base import BaseCommand, CommandError
from api.models.match import Match, MatchIA


class Command(BaseCommand):
    help = 'Given a match id, prints match status'

    def clear(self):
        os.system("clear")

    def add_arguments(self, parser):
            parser.add_argument(
                "--match-id",
                required=True,
                type=int
            )

    def handle(self, *args, **options):
        query_set = (
            MatchIA.objects.
            filter(match=options['match_id']).
            order_by("-ia__name")
        )
        if not query_set.exists():
            return CommandError(f"There is not match with id {options['match_id']}")

        match = Match.objects.get(id=options["match_id"])
        while True:
            msg = "==================================================\n"
            msg += f"{datetime.datetime.now()} - Match {match.name}\n"
            for match_ia in query_set.iterator():
                msg += (
                    f"IA: {match_ia.ia.name} \n"
                    f"\t zone {match_ia.where_am_i.name}({match_ia.where_am_i.id}) \n" 
                    f"\t live {match_ia.life}. \n"
                    f"\t Is alive: {match_ia.alive}\n"
                )
            msg += "=================================================="
            self.clear()
            print(msg, flush=True)
            sleep(1)
