#!/usr/bin/env python
import unittest

import django.test
from django.http import Http404

from django.test import TestCase
from django.contrib.auth.models import User

from api.models.match import Match
from api.models.map import Map
from api.models.ia import IA

from web.views import zones


class TestApi(TestCase):

    def setUp(self):
        self.map = Map(name="Map name")
        self.map.save()

        self.user = User()
        self.user.save()

        self.ia1 = IA(
            user=self.user,
            name="IA1"
        )
        self.ia1.save()

        self.match = Match(
            name="match name",
            map=self.map
        )
        self.match.save()

    def test_zone_view(self):
        invented_match_id = 232323
        request = django.test.RequestFactory()
        with self.assertRaises(Http404):
            zones(request, invented_match_id)

    def test_BattleRoyal_map_not_exists(self):
        request = django.test.RequestFactory()
        self.assertTrue(
            Match.objects.get(id=self.match.id) is not None
        )
        with self.assertRaises(Http404):
            zones(request, self.match.id)

    def test_no_errors_when_BattleRoyal_map_exists(self):

        battle_royal = Map(name="Battle Royal")
        battle_royal.save()
        request = django.test.RequestFactory()
        zones(request, self.match.id)
