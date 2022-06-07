# IA Actions contract

##  Basic Actions
You can do all the get requests that the IA want it, but only one POST each X seconds(Maybe 2?).
actives actions > POST
pasive actions > GET

### Attack(active)
Only can attack another IA in your same zone.

### Defend(pasive)
If you are defending you halve the damage.

### Investigate(pasive)
If you investigate a zone you can get hte information about how many players are in that zone and items.
{
    zone: a
    'players': [paquito, jose, myself],
    'items': [pocion de vida, hacha],
    'neighbours: [b,c,f]
}

### Catch(active)
to catch an item in your zone

### Stats(pasive)
Information about your health

### Move(active)
You can move to a neighbour zone.


## Maps

TODO
Every battle happens in a map split in zones, in each zone we can have one or more items or players.


## Items

TODO