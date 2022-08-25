# IA Actions contract

##  Basic Actions
You can do all the get requests that the IA want it, but only one POST each X seconds(Maybe 2?).
actives actions > POST
pasive actions > GET

### Attack(active)
Only can attack another IA in your same zone.

#### POST

##### request
- attack_to: ID ia to attack
- match: match id where to attack, a player can play multiple matches at the same time

```
{
    "attack_to": 3,  
    "match": 5
}
```

##### response:
- damage: amount of damage that the attack did
- timestamp: when the damage was write it in the database

```
{
    "attack_to": 3,  
    "match": 5
}
```

### Defend(pasive)
If you are defending you halve the damage.

#### GET

##### request
- whithout parameters

##### response:
- shield: amount of damage your shield can reduce from an attack
- timestamp: the last time that your shield suffered a change
- active: true if it's enable false if not

```
{
    "shield": 5,
    "timestamp": 34234234,
    "active": true
}
```
#### POST

##### request
- active: value to set in your shield

```
{
    "active": true
}
```

##### response:
- shield: amount of damage your shield can reduce from an attack
- timestamp: the last time that your shield suffered a change
- active: true if it's enable false if not

```
{
    "shield": 5,
    "timestamp": 34234234,
    "active": true
}
```


### Investigate(pasive)
If you investigate a zone you can get the information about how many players are in that zone.

#### GET

##### request
- /finds

##### response:
- players: list of players in the zone actually
- neighbours: id's zones where you can go from this zone
- timestamp: timestamp of the request

```
{
    "ias": [PLAYER_ID_1, PLAYER_ID_2,...,PLAYER_ID_N],
    "neighbours": [ZONE_ID_1, ZONE_ID_2,...,ZONE_ID_N],
    "timestamp": 37452837
}
```

### Catch(active)
TODO


### Stats(pasive)
Information about your health

#### GET

##### request
whithout parameters

##### response:
- health: amount of health that you have actually
- zone: zone id where you are
- timestamp: timestamp of the request

```
{
    "health": 46
    "zone": 3,
    "timestamp": 37452837
}
```


### Move(active)
You can move to a neighbour zone.

#### POST

##### request
- zone: zone id where do you want go

```
{
    "zone": 4
}
```

##### response:
- players: list of players in the zone actually
- neighbours: id's zones where you can go from this zone
- timestamp: timestamp of the request

```
{
    "players": [PLAYER_ID_1, PLAYER_ID_2,...,PLAYER_ID_N],
    "neighbours": [ZONE_ID_1, ZONE_ID_2,...,ZONE_ID_N],
    "timestamp": 37452837
}
```


## Maps

Every battle happens in a map split in zones, in each zone we can have one or more items or players.


## Items

TODO