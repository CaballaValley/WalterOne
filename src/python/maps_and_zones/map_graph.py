from api.models import Zone, Map


royal_map = royal_map = Map.objects.get(name="Battle Royal")
zones = Zone.objects.filter(map=royal_map).order_by("name")

for i, zone in enumerate(zones, 1):
    n_neighbors = zone.neighbors.count()
    neighbors = ', '.join([z.name for z in zone.neighbors.all()])
    lucky_unlucky_trigger = f"\tlucky_unlucky: {zone.lucky_unlucky}"
    go_ryu = f"\tgo_ryu: {zone.go_ryu}"
    karin_gift = f"\tkarin_gift: {zone.karin_gift}"

    print(f"{i} zone {zone.name}")
    print(f"Neighbours ({n_neighbors}): {neighbors}")
    print(lucky_unlucky_trigger)
    print(go_ryu)
    print(karin_gift)
