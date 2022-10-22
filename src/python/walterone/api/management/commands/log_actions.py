#!/usr/bin/env python
from datetime import datetime, timedelta
import time
import pytz
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from api.models.action import (
    Attack,
    Move,
)


class Command(BaseCommand):

    AVAILABLE_ACTIONS_MOVEMENTS = {
        "moves": Move,
        "attacks": Attack,
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--event_type',
            type=str,
            required=True,
        )

        parser.add_argument(
            '--sleeping_seconds',
            type=int,
            default=5,
        )

        parser.add_argument(
            '--last_actions_seconds',
            type=int,
            default=60*5,
        )

        parser.add_argument(
            '--match_id',
            type=int,
            required=True,
        )

    def query_print_and_sleep(self, action_model, time_sleep,
                              last_action_seconds, match_id):
        # Query
        while True:
            start = timezone.now() - timedelta(seconds=last_action_seconds)
            end = timezone.now()
            actions = action_model.objects.filter(
                timestamp__range=(start, end),
                match_id=match_id,
            )

            if actions:
                actions_msg = '\n'.join([str(action) for action in actions])
                print(actions_msg)
            else:
                print(f"No actions on match {match_id} last {last_action_seconds/60} minutes )")
            print(f"================ sleeping {time_sleep} seconds =======================")
            time.sleep(time_sleep)

    def handle(self, *args, **options):
        # Check arguments
        movement_type = options["event_type"]
        if movement_type not in self.AVAILABLE_ACTIONS_MOVEMENTS:
            raise CommandError(
                f"Action type '{movement_type}' not valid. Available actions are: "
                f"{', '.join(self.AVAILABLE_ACTIONS_MOVEMENTS.keys())}"
            )

        try:
            self.query_print_and_sleep(
                time_sleep=options["sleeping_seconds"],
                action_model=self.AVAILABLE_ACTIONS_MOVEMENTS[movement_type],
                last_action_seconds=options["last_actions_seconds"],
                match_id=options["match_id"],
            )
        except KeyboardInterrupt:
            print("Shutting down...")
            return
