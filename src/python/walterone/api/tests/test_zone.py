from django.test import TestCase

from api.models.map import Map
from api.models.zone import Zone


class ZoneTestCase(TestCase):
    def setUp(self):
        map_instance = Map.objects.create(name="Andalucia")
        Zone.objects.create(
            name="huelva",
            map=map_instance,
            lucky_unlucky=True,
            go_ryu=True)
        Zone.objects.create(
            name="sevilla",
            map=map_instance,
            karin_gift=True)

    def test_create_neighbors(self):
        huelva = Zone.objects.get(name="huelva")
        neighbors = huelva.neighbors.all()
        self.assertEqual(len(neighbors), 0)

        sevilla = Zone.objects.get(name="sevilla")
        huelva.neighbors.add(sevilla)
        neighbors = huelva.neighbors.all()
        self.assertEqual(len(neighbors), 1)
